#!/usr/bin/env python
# encoding: utf-8

# disable:
# - R0902,too many instance attributes: This is a stats class
# pylint: disable=R0902

"""This module handle ELO player stats
"""

from collections import Counter


class StatsPlayer(object):
    """A player stat"""

    def __init__(self, name):
        super(StatsPlayer, self).__init__()
        self.name = name
        self.win = 0
        self.last = 0
        self.beaten_by = []
        self.elo = 0
        self.games = []
        self.plays_number = 0
        self.streak_win = 0
        self.streak_win_longest = 0
        self.streak_loose = 0
        self.streak_loose_longest = 0
        self.win_play_per_game = {}

    def set_elo(self, new_elo):
        """Elo is set by EloStat
        :type new_elo: int"""
        self.elo = new_elo

    def new_play(self, play):
        """
        handle a new play in stats
        :param play:    The new play to add to the stats
        """
        has_won = False
        if self.name in play.get_winners():
            has_won = True
            self.new_win()
        else:
            self.new_loss(play.get_winners())
        self.plays_number += 1
        self.games.append(play.game)
        if self.name in play.get_player_order()[-1][1]:
            self.last += 1
        # store win per game stats
        if play.game not in self.win_play_per_game:
            self.win_play_per_game[play.game] = [0, 0]
        per_game_stat = self.win_play_per_game[play.game]
        if has_won:
            per_game_stat[0] = per_game_stat[0] + 1
        per_game_stat[1] = per_game_stat[1] + 1

    def new_win(self):
        """
        a new win !
        """
        self.win += 1
        self.streak_win += 1
        if self.streak_win > self.streak_win_longest:
            self.streak_win_longest = self.streak_win
        if self.streak_loose > 0:
            self.streak_loose = 0

    def new_loss(self, winners):
        """
        a new loss, bouh !
        """
        self.beaten_by.extend(winners)
        self.streak_loose += 1
        if self.streak_loose > self.streak_loose_longest:
            self.streak_loose_longest = self.streak_loose
        if self.streak_win > 0:
            self.streak_win = 0

    def __str__(self):
        "return a string representation"
        return '%10s\t%20s\t%20s' % (self.name,
                                     self.win,
                                     self.plays_number)

    def get_percentage(self):
        "return the percentage of victory"
        return int(100 * (float(self.win) / float(self.plays_number)))

    def get_worst_ennemy(self):
        """
        return the player who beat most time as a tuple (player, defeatnb)
        :return: a tuple (player, defeatnb)
        """
        most_commons = Counter(self.beaten_by).most_common(n=1)
        if most_commons != []:
            return Counter(self.beaten_by).most_common(n=1)[0]
        # when no one has ever beaten the player
        return 'none', 0

    def get_most_played_game(self):
        "return the player who beat most time (player, defeatnb)"
        return Counter(self.games).most_common(n=1)[0]

    def to_json(self):
        """Return the json version of this
        :rtype: dict[str, obj]"""

        # transform win per games to a json - like array
        win_per_games = []
        for game in self.win_play_per_game:
            win, play_nb = self.win_play_per_game[game]
            win_per_games.append({
                'game': game,
                'win': win,
                'play_nb': play_nb,
                'win_percentage': round(float(win) / play_nb * 100, 2)
            })
        return {
            'name': self.name,
            'win': self.win,
            'last': self.last,
            'beaten_by': self.beaten_by,
            'elo': self.elo,
            'games': self.games,
            'plays_number': self.plays_number,
            'streak_win': self.streak_win,
            'streak_win_longest': self.streak_win_longest,
            'streak_loose': self.streak_loose,
            'streak_loose_longest': self.streak_loose_longest,
            'win_play_per_game': win_per_games
        }
