#!/usr/bin/env python
# encoding: utf-8

"Handles scores"

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from collections import Counter
import operator
import os
import yaml


from helper import required_fields


THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEMPLATE_DIR = os.path.join(THIS_DIR, '..', 'templates')


class Scores(object):
    """docstring for Scores"""
    def __init__(self, filename=None):
        super(Scores, self).__init__()
        self.plays = []
        if filename is not None:
            self.load(filename)

    def __str__(self):
        "returns string representation"
        return "%s" % '\n'.join([str(play) for play in self.plays])

    def load(self, filename='scores.yml'):
        """
        Load the given filename under YAML format

        :param filename: The filename to find the YAML
        """
        with open(filename) as yml_file:
            # loading yaml.safe_load ensure byte str instead of unicode string
            yml_data = yaml.safe_load(yml_file)
            play_id = 0
            for json_play in yml_data:
                new_play = Play(yml_data=json_play)
                new_play.play_id = play_id
                self.plays.append(new_play)
                play_id += 1

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
                if player.name not in players:
                    players.append(player.name)
        return players

    def get_plays(self):
        """
        :rtype: list[Play]
        :return: The plays
        """
        return self.plays

    def add_play(self, play):
        """Add a new Play.
        :type play: Play
        :rtype: void
        """
        self.plays.append(play)


class Play(object):
    """A Play is a board game instance with players and scores.
    """
    id_counter = 0

    def __init__(self, yml_data=None):
        super(Play, self).__init__()
        self.play_id = Play.id_counter
        Play.id_counter += 1
        self.date = '01/01/1977'
        self.game = 'nogame'
        self.players = []
        self.winners = None
        if yml_data is not None:
            self.from_json(yml_data)

    def __str__(self):
        "return string representation of the Play"
        sorted_players = sorted(self.players,
                                key=lambda p: p.score,
                                reverse=True)

        return "[%03d]%s: %s %s" % (self.play_id, self.date,
                                    self.game,
                                    ', '.join(['%s(%s)' % (player.name,
                                                           player.score)
                                              for player in sorted_players]))

    @required_fields(['date', 'game'])
    def from_json(self, data):
        """
        loads json datas
        :param data: The json datas
        :return:
        """
        self.date = data['date']
        self.game = data['game']
        self.players = []
        self.winners = None
        for player_json in data['players']:
            self.players.append(Player(yml_data=player_json))
        if 'winners' in data:
            self.winners = data['winners']
        if 'type' in data:
            self.type = data['type']

    def to_json(self):
        "serialize to json"
        yml_data = {"id": self.play_id,
                    "date": self.date,
                    "game": self.game}
        if hasattr(self, 'winners') and self.winners is not None:
            yml_data['winners'] = self.winners
        if hasattr(self, 'type') and self.type is not None:
            yml_data['type'] = self.type
        yml_data['players'] = [player.to_json()
                               for player in self.players]
        return yml_data

    def get_player_order(self):
        "return a list of tuple [(score, [players])] ordered per score"
        player_per_score = {}
        for (player, score) in [(player.name, player.score)
                                for player in self.players]:
            if score not in player_per_score:
                player_per_score[score] = []
            player_per_score[score].append(player)
        if hasattr(self, 'type') and self.type == 'min':
            return sorted(player_per_score.items(), key=lambda x: x[0])
        return sorted(player_per_score.items(),
                      key=lambda x: x[0], reverse=True)

    def get_winners(self):
        "return the list of player names that wins the play"
        if self.winners is not None and isinstance(self.winners, list):
            return self.winners
        elif self.winners is not None:
            raise TypeError('Expected type for winners is list but found %s' %
                            type(self.winners))
        return self.get_player_order()[0][1]

    def get_highest_score(self):
        "return the high score of the play"
        return self.get_player_order()[0][0]

    def get_lowest_score(self):
        "return the lowest score of the play"
        return self.get_player_order()[-1][0]


class Player(object):
    """docstring for Player"""
    def __init__(self, name='noname', score=0, team=None, yml_data=None):
        super(Player, self).__init__()
        self.name = name
        self.score = int(score)
        self.team = team
        self.team_color = None
        self.color = None
        if yml_data is not None:
            self.__load_json(yml_data)

    def __str__(self):
        """return string representation of the Player
        :rtype: str
        """
        return "%s(%s)" % (self.name,
                           self.score)

    def to_json(self):
        """serialize to json
        :rtype: dict[str, str]"""
        yml_data = {"name": self.name,
                    "score": self.score}
        if self.team:
            yml_data['team'] = self.team
        if self.team_color:
            yml_data['team_color'] = self.team_color
        if self.color:
            yml_data['color'] = self.color
        return yml_data

    def __load_json(self, yml_data):
        "loads json"
        self.name = yml_data['name']
        self.score = yml_data['score']
        if 'team' in yml_data:
            self.team = yml_data['team']
        if 'team_color' in yml_data:
            self.team_color = yml_data['team_color']
        if 'color' in yml_data:
            self.color = yml_data['color']

    def dummy_pep8(self):
        """
        this is dummy
        """
        pass


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
        self.scores.extend([player.score for player in play.players])
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
        scores = [player.score for player in play.players]
        self.scores_per_number[player_nb].extend(scores)

        # add scores per player
        for player in play.players:
            if player.name not in self.scores_per_player:
                self.scores_per_player[player.name] = []
            self.scores_per_player[player.name].append(player.score)

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
            'highest_score_play_id': self.highest_score_play.play_id,
            'highest_score_play_players':
                self.highest_score_play.get_winners(),
            'lowest_score': self.lowest_score_play.get_lowest_score(),
            'lowest_score_play_id': self.lowest_score_play.play_id,
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
            if player.name not in self.player_stats:
                self.player_stats[player.name] = PlayerStat(player.name)
            self.player_stats[player.name].new_play(play)
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
        return template.render(title=u'GAME STATS', stats=self)
