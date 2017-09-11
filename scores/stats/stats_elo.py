#!/usr/bin/env python
# encoding: utf-8

"""This module handle ELO stats
"""

import logging

import scores.elo as elo

LOGGER = logging.getLogger(__name__)

# The K factor is used to tune the ELO gain/loose
K_FACTOR = 40
# The initial ELO is the ELO score of new players
INITIAL_ELO = 1000


class StatsElo(object):
    """To follow ELO score of players"""

    def __init__(self):
        super(StatsElo, self).__init__()
        self.elos_per_player = dict()
        self.elos_per_play = dict()

    def new_play(self, play):
        """
        handle a new play in stats
        :param play:    The new play to add to the stats
        """
        teams = play.teams

        if len(teams.keys()) > 1:
            self.__compute_elo_team(play, teams)
        else:
            self.__compute_elo_player(play)

    def __compute_elo_team(self, play, teams):
        """Compute ELOS for a play with teams"""
        # Compute team score
        scores_per_team = []
        # Retrieve Team infos
        for team in teams:
            players = teams[team]
            team_score = 0
            team_elo = 0
            for login in players:
                if login not in self.elos_per_player:
                    LOGGER.debug('adding login %s', login)
                    self.elos_per_player[login] = INITIAL_ELO
                player_score = play.get_player(login)['score']
                player_elo = self.elos_per_player[login]
                team_score += player_score
                team_elo += player_elo
            # make it average
            team_score = team_score / len(players)
            team_elo = team_score / len(players)
            team_size = len(players)
            scores_per_team.append((team, team_score, team_elo, team_size))
        # order teams by scores
        if play.is_max:
            scores_per_team = sorted(scores_per_team, key=lambda x: x[1], reverse=True)
        else:
            scores_per_team = sorted(scores_per_team, key=lambda x: x[1])

        # compute teams rank
        # teams are sorted, but they could have same score
        # compute rank of the team by parsing teams, and using rank of previous
        # team is score is the same
        previous_score = None
        team_rank = range(1, len(scores_per_team) + 1)
        for index, team in enumerate(scores_per_team):
            team_score = team[1]
            if team_score == previous_score:
                team_rank[index] = team_rank[index - 1]
            else:
                team_rank[index] = index
            previous_score = team_score
        # The K factor must be multiplied by the max number of ppl in a team
        # Because points will be shared accross the team.
        max_team_size = max(scores_per_team, key=lambda item: item[3])
        # Finally, compute ELOS
        elo_diff = elo.compute_elos([item[2] for item in scores_per_team],
                                    team_rank,
                                    int(K_FACTOR * max_team_size[3]))
        # Now apply elo_diff to the players
        elos_per_player = {}
        for index, diff in enumerate(elo_diff):
            team = scores_per_team[index][0]
            team_size = scores_per_team[index][3]
            # get players for this team
            player_logins = teams[team]
            for login in player_logins:
                base_elo = self.elos_per_player[login]
                final_elo = base_elo + int(diff / team_size)
                elos_per_player[login] = (base_elo, final_elo)
                self.elos_per_player[login] = final_elo
        self.elos_per_play[play.id] = elos_per_player

    def __compute_elo_player(self, play):
        """Compute elo for a play without teams"""
        oplayers = []
        elos = []
        rank = []
        current_rank = 0
        for _, player_list in play.get_player_order():
            for login in player_list:
                if login not in self.elos_per_player:
                    self.elos_per_player[login] = INITIAL_ELO
                oplayers.append(login)
                elos.append(self.elos_per_player[login])
                rank.append(current_rank)
            current_rank += 1
        # Compute ELO variations
        elo_diff = elo.compute_elos(elos, rank, 40)
        # apply new Elos and save them to play
        elos_per_player = {}
        for index, login in enumerate(oplayers):
            base_elo = self.elos_per_player[login]
            final_elo = base_elo + elo_diff[index]
            elos_per_player[login] = (base_elo, final_elo)
            self.elos_per_player[login] = final_elo
        self.elos_per_play[play.id] = elos_per_player

    def get_elo(self, login):
        """Returnt the ELO of a login
        :rtype: int
        """
        return self.elos_per_player[login]

    def get_elos_per_player(self, play_id):
        """Return the elos per player of the given play
        :rtype: dict(basestring, tuple(int, int))"""
        return self.elos_per_play[play_id]
