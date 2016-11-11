#!/usr/bin/env python
# encoding: utf-8

"Handles scores"

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from collections import Counter
from .database import Database
import operator
import os
import yaml


from helper import required_fields


THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEMPLATE_DIR = os.path.join(THIS_DIR, '..', 'templates')


class Scores(object):
    """docstring for Scores"""

    def __init__(self, database=None):
        """Init
        :type database: Database
        """
        super(Scores, self).__init__()
        self.plays = []
        if database is not None:
            self.plays.extend(database.get_plays())

    def __str__(self):
        "returns string representation"
        return "%s" % '\n'.join([str(play) for play in self.plays])

    def dump(self, filename='scores.yml'):
        """
        dumps the scores into given filename

        @param filename the filename to dump to
        """
        with open(filename, 'w') as yaml_file:
            yaml.dump(self.to_json(), yaml_file)

    def to_json(self):
        "transform object to json"
        return [play.to_json() for play in self.plays]

    def get_games(self):
        """
        :return: a set of game names
        """
        return frozenset([play.game for play in self.plays])

    def get_players(self):
        """
        return a set of players
        :return: a set of players
        """
        players = []
        for play in self.plays:
            for player in play.players:
                login = player['login']
                if login not in players:
                    players.append(login)
        return players

    def get_plays(self):
        """
        :rtype: list[Play]
        :return: The plays
        """
        return self.plays

    def get_play(self, play_id):
        for play in self.plays:
            if play.id == play_id:
                return play

    def add_play(self, play):
        """Add a new Play.
        :type play: Play
        :rtype: void
        """
        self.plays.append(play)


class GameStat(object):
    """A game stat"""

    def __init__(self, game):
        super(GameStat, self).__init__()
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
        if (hasattr(self.highest_score_play, 'type') and
                self.highest_score_play.type == 'min'):
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


class PlayerStat(object):
    """A player stat"""

    def __init__(self, name):
        super(PlayerStat, self).__init__()
        self.name = name
        self.win = 0
        self.last = 0
        self.beaten_by = []
        self.games = []
        self.plays_number = 0
        self.streak_win = 0
        self.streak_win_longest = 0
        self.streak_loose = 0
        self.streak_loose_longest = 0

    def new_play(self, play):
        """
        handle a new play in stats
        :param play:    The new play to add to the stats
        """
        if self.name in play.get_winners():
            self.__new_win()
        else:
            self.__new_loss(play.get_winners())
        self.plays_number += 1
        self.games.append(play.game)
        if self.name in play.get_player_order()[-1][1]:
            self.last += 1

    def __new_win(self):
        """
        a new win !
        """
        self.win += 1
        self.streak_win += 1
        if self.streak_win > self.streak_win_longest:
            self.streak_win_longest = self.streak_win
        if self.streak_loose > 0:
            self.streak_loose = 0

    def __new_loss(self, winners):
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
        if len(most_commons) > 0:
            return Counter(self.beaten_by).most_common(n=1)[0]
        # when no one has ever beaten the player
        return 'none', 0

    def get_most_played_game(self):
        "return the player who beat most time (player, defeatnb)"
        return Counter(self.games).most_common(n=1)[0]

    def to_json(self):
        """Return the json version of this
        :rtype: dict[str, obj]"""
        return {
            'name': self.name,
            'win': self.win,
            'last': self.last,
            'beaten_by': self.beaten_by,
            'games': self.games,
            'plays_number': self.plays_number,
            'streak_win': self.streak_win,
            'streak_win_longest': self.streak_win_longest,
            'streak_loose': self.streak_loose,
            'streak_loose_longest': self.streak_loose_longest,
        }


class OverallWinnerStat(object):
    """Gets the overall number of victory """

    def __init__(self):
        super(OverallWinnerStat, self).__init__()
        self.player_stats = {}
        self.game_stats = {}
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
        for player in play.players:
            login = player['login']
            if login not in self.player_stats:
                self.player_stats[login] = PlayerStat(login)
            self.player_stats[login].new_play(play)
        if play.game not in self.game_stats:
            self.game_stats[play.game] = GameStat(play.game)
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

    def to_html(self, filename='target/site/index.html'):
        """
        generate scores stats as html page
        :param filename: The name of the html file to be generated
        :return:
        """
        menv = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = menv.get_template('index.html')
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'w') as output:
            output.write(self.get_html().encode('UTF-8'))

    def get_html(self):
        " return the html"
        menv = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = menv.get_template('index.html')
        return template.render(title=u'GAME STATS',
                               stats=self,
                               current_user='none')
