#!/usr/bin/env python
# encoding: utf-8

"Handles scores"

from jinja2 import Environment
from jinja2.loaders import PackageLoader
from collections import Counter
import os
import yaml


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
        "Load the given filename under YAML format"
        with open(filename) as yml_file:
            # loading yaml.safe_load ensure byte str instead of unicode string
            yml_data = yaml.safe_load(yml_file)
            print yml_data
            for json_play in yml_data:
                self.plays.append(Play(yml_data=json_play))

    def dump(self, filename='scores.yml'):
        "dumps the scores into given filename"
        with open(filename, 'w') as yaml_file:
            yaml.dump(self.to_json(), yaml_file)

    def to_json(self):
        "transform object to json"
        return [play.to_json() for play in self.plays]


class Play(object):
    """docstring for ClassName"""
    def __init__(self, yml_data=None):
        super(Play, self).__init__()
        self.date = '01/01/1977'
        self.game = 'nogame'
        self.players = []
        self.winners = []
        if yml_data is not None:
            self.__load_json(yml_data)

    def __str__(self):
        "return string representation of the Play"
        sorted_players = sorted(self.players,
                                key=lambda p: p.score,
                                reverse=True)

        return "%s: %s %s" % (self.date,
                              self.game,
                              ', '.join(['%s(%s)' % (player.name, player.score)
                                         for player in sorted_players]))

    def __load_json(self, yml_data):
        "loads json datas"
        self.date = yml_data['date']
        self.game = yml_data['game']
        self.players = []
        self.winners = None
        for player_json in yml_data['players']:
            self.players.append(Player(yml_data=player_json))
        if 'winners' in yml_data:
            self.winners = yml_data['winners']
        if 'type' in yml_data:
            self.type = yml_data['type']

    def to_json(self):
        "serialize to json"
        if isinstance(self, Play):
            yml_data = {"date": self.date,
                        "game": self.game}
            if hasattr(self, 'winners') and self.winners is not None:
                yml_data['winners'] = self.winners
            if hasattr(self, 'type') and self.type is not None:
                yml_data['type'] = self.type
            yml_data['players'] = [player.to_json()
                                   for player in self.players]
            return yml_data
        raise TypeError(repr(self) + " cannot be serialized")

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
        self.score = score
        self.team = team
        if yml_data is not None:
            self.__load_json(yml_data)

    def __str__(self):
        "return string representation of the Play"
        return "%s(%s)" % (self.name,
                           self.score)

    def to_json(self):
        "serialize to json"
        if isinstance(self, Player):
            yml_data = {"name": self.name,
                        "score": self.score}
            if self.team:
                yml_data['team'] = self.team
            return yml_data
        raise TypeError(repr(self) + " cannot be serialized")

    def __load_json(self, yml_data):
        "loads json"
        self.name = yml_data['name']
        self.score = yml_data['score']
        if 'team' in yml_data:
            self.team = yml_data['team']

    def dummy(self):
        "dummy"
        pass


class GameStat(object):
    """A game stat"""
    def __init__(self, game):
        super(GameStat, self).__init__()
        self.game = game
        self.plays_number = 0
        self.highest_score_play = None
        self.lowest_score_play = None

    def new_play(self, play):
        "handle a new play in stats"
        self.plays_number = self.plays_number + 1
        if (self.highest_score_play is None or
            (play.get_highest_score() >
                self.highest_score_play.get_highest_score())):
            self.highest_score_play = play
        if (self.lowest_score_play is None or
            (play.get_lowest_score() <
                self.lowest_score_play.get_lowest_score())):
            self.lowest_score_play = play

    def get_highest_score(self):
        "return the play that had the highest score"
        return self.highest_score_play

    def get_lowest_score(self):
        "return the play that had the lowest score"
        return self.lowest_score_play


class PlayerStat(object):
    """A player stat"""
    def __init__(self, name):
        super(PlayerStat, self).__init__()
        self.name = name
        self.win = 0
        self.beaten_by = []
        self.games = []
        self.plays_number = 0

    def new_play(self, play):
        "handle a new play in stats"
        if self.name in play.get_winners():
            self.win = self.win + 1
        else:
            self.beaten_by.extend(play.get_winners())

        self.plays_number = self.plays_number + 1
        self.games.append(play.game)

    def __str__(self):
        "return a string representation"
        return '%10s\t%20s\t%20s' % (self.name,
                                     self.win,
                                     self.plays_number)

    def get_percentage(self):
        "return the percentage of victory"
        return int(100 * (float(self.win) / float(self.plays_number)))

    def get_worst_ennemy(self):
        "return the player who beat most time (player, defeatnb)"
        most_commons = Counter(self.beaten_by).most_common(n=1)
        if len(most_commons) > 0:
            return Counter(self.beaten_by).most_common(n=1)[0]
        # when no one has ever beaten the player
        return ('none', 0)

    def get_most_played_game(self):
        "return the player who beat most time (player, defeatnb)"
        return Counter(self.games).most_common(n=1)[0]


class OverallWinnerStat(object):
    """Gets the overall number of victory """
    def __init__(self):
        super(OverallWinnerStat, self).__init__()
        self.player_stats = {}
        self.game_stats = {}
        self.plays = []

    def parse(self, scores):
        "parse given scores"
        for play in scores.plays:
            self.new_play(play)

    def new_play(self, play):
        "handle a new play in this stat"
        self.plays.append(play)
        for player in play.players:
            if player.name not in self.player_stats:
                self.player_stats[player.name] = PlayerStat(player.name)
            self.player_stats[player.name].new_play(play)
        if play.game not in self.game_stats:
            self.game_stats[play.game] = GameStat(play.game)
        self.game_stats[play.game].new_play(play)

    @staticmethod
    def description():
        "return the stat header"
        return "# Overall victories"

    def __str__(self):
        "to string !"
        result = self.description() + '\n'
        result = result + '%10s;%20s;%20s;%10s' % ('name',
                                                   'victoires',
                                                   'participations',
                                                   'pourcentage V')

        for item in sorted(self.player_stats.values(),
                           key=lambda x: x.win, reverse=True):
            result = result + '\n%10s;%20s;%20s;%10s' % (item.name,
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
        " generate scores stats as html page"
        menv = Environment(loader=PackageLoader('scores', 'templates'))
        template = menv.get_template('index.html')
        if not os.path.exists('target/site'):
            os.makedirs('target/site')
        with open(filename, 'w') as output:
            output_str = template.render(title=u'GAME STATS',
                                         stats=self)
            output.write(output_str.encode('UTF-8'))

    def get_html(self):
        " return the html"
        menv = Environment(loader=PackageLoader('scores', 'templates'))
        template = menv.get_template('index.html')
        return template.render(title=u'GAME STATS', stats=self)

if __name__ == '__main__':
    MSCORES = Scores(filename='scores.yml')
    STATS = OverallWinnerStat()
    STATS.parse(MSCORES)
    STATS.to_html()
