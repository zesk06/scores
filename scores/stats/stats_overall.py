#!/usr/bin/env python
# encoding: utf-8

"""This module handle ELO overall stats
"""


import scores.stats.stats_elo as stats_elo
import scores.stats.stats_player as stats_player
import scores.stats.stats_game as stats_game


class OverallWinnerStat(object):
    """Gets the overall number of victory """

    def __init__(self):
        super(OverallWinnerStat, self).__init__()
        self.player_stats = {}
        self.game_stats = {}
        self.elo_stats = stats_elo.StatsElo()
        self.plays = []

    def parse(self, scores):
        """
        parse given scores
        :param scores: the scores to be parsed
        :return:
        """
        for play in scores.plays:
            self.new_play(play)

    def new_play(self, play):
        """
        handle a new play in this stat
        :param play: The play to be added to the stats
        :return:
        """
        self.plays.append(play)
        self.elo_stats.new_play(play)
        for player in play.players:
            login = player['login']
            if login not in self.player_stats:
                self.player_stats[login] = stats_player.StatsPlayer(login)
            self.player_stats[login].new_play(play)
            self.player_stats[login].set_elo(self.elo_stats.get_elo(login))
        if play.game not in self.game_stats:
            self.game_stats[play.game] = stats_game.StatsGame(play.game)
        self.game_stats[play.game].new_play(play)

    def __str__(self):
        "to string !"
        result = '%10s;%20s;%20s;%10s' % ('name',
                                          'victoires',
                                          'participations',
                                          'pourcentage V')

        for item in sorted(self.player_stats.values(),
                           key=lambda x: x.win, reverse=True):
            result += '\n%10s;%20s;%20s;%10s' % (item.name,
                                                 item.win,
                                                 item.plays_number,
                                                 item.get_percentage())
        return result

    def get_sorted_players(self):
        "return the players, sorted by win"
        return sorted(self.player_stats.values(),
                      key=lambda x: x.win,
                      reverse=True)
