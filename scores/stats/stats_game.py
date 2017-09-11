#!/usr/bin/env python
# encoding: utf-8

# disable:
# - R0902,too many instance attributes: This is a stats class
# pylint: disable=R0902

"""This module handle ELO Game stats
"""

import operator


class StatsGame(object):
    """A game stat"""

    def __init__(self, game):
        super(StatsGame, self).__init__()
        self.game = game
        self.plays_number = 0
        self.highest_score_play = None
        self.lowest_score_play = None
        self.scores = []
        self.victories_per_player = {}
        self.scores_per_player = {}
        self.scores_per_number = {}

    def new_play(self, play):
        """
        Handle a new play
        :param play:  The play to add
        :return: nothing
        """
        self.plays_number += 1
        self.scores.extend([player['score'] for player in play.players])
        if self.highest_score_play is None:
            self.highest_score_play = play
        if self.lowest_score_play is None:
            self.lowest_score_play = play
        if self.highest_score_play.wintype == 'min':
            if (play.get_highest_score() <
                    self.highest_score_play.get_highest_score()):
                self.highest_score_play = play
            if (play.get_lowest_score() >
                    self.lowest_score_play.get_lowest_score()):
                self.lowest_score_play = play
        else:
            if (play.get_highest_score() >
                    self.highest_score_play.get_highest_score()):
                self.highest_score_play = play
            if (play.get_lowest_score() <
                    self.lowest_score_play.get_lowest_score()):
                self.lowest_score_play = play

        # count victories for the player
        for player in play.get_winners():
            if player not in self.victories_per_player:
                self.victories_per_player[player] = 0
            self.victories_per_player[player] += 1
        # add score per number of players
        player_nb = len(play.players)
        if player_nb not in self.scores_per_number:
            self.scores_per_number[player_nb] = []
        scores = [player['score'] for player in play.players]
        self.scores_per_number[player_nb].extend(scores)

        # add scores per player
        for player in play.players:
            login = player['login']
            if login not in self.scores_per_player:
                self.scores_per_player[login] = []
            self.scores_per_player[login].append(player['score'])

    def get_highest_score(self):
        "return the play that had the highest score"
        return self.highest_score_play

    def get_lowest_score(self):
        "return the play that had the lowest score"
        return self.lowest_score_play

    def get_average_score(self):
        "return the average score"
        return sum(self.scores) / len(self.scores)

    def get_best_player(self):
        """
        return the player with the maximum number of victories
        :return: the player with the maximum number of victories
        """
        return sorted(self.victories_per_player, key=operator.itemgetter(1))[0]

    def to_json(self):
        """Return the json version of this"""
        lower_score_players = self.lowest_score_play.get_player_order()[-1][1]
        return {
            'game': self.game,
            'plays_number': self.plays_number,
            'highest_score': self.highest_score_play.get_highest_score(),
            'highest_score_play_id': self.highest_score_play.id,
            'highest_score_play_players':
                self.highest_score_play.get_winners(),
            'lowest_score': self.lowest_score_play.get_lowest_score(),
            'lowest_score_play_id': self.lowest_score_play.id,
            'lowest_score_play_players': lower_score_players,
            'scores_per_number': self.scores_per_number,
            'scores_per_player': self.scores_per_player,
            'victories_per_player': self.victories_per_player
        }
