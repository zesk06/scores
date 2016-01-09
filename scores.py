#!/usr/bin/env python
# encoding: utf-8

"Handles scores"

import json


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

    def load(self, filename='scores.json'):
        "Load the given filename under json format"
        with open(filename) as json_file:
            json_data = json.load(json_file)
            for json_play in json_data:
                self.plays.append(Play(json_play))

    def dump(self, filename='scores_bis.py'):
        "dumps the scores into given filename"
        with open(filename, 'w') as json_file:
            json.dump(self.to_json(), json_file, indent=4, sort_keys=True)

    def to_json(self):
        "transform object to json"
        return [play.to_json() for play in self.plays]


class Play(object):
    """docstring for ClassName"""
    def __init__(self, json_data=None):
        super(Play, self).__init__()
        self.date = '01/01/1977'
        self.game = 'nogame'
        self.players = []
        self.winners = []
        if json_data is not None:
            self.__load_json(json_data)

    def __str__(self):
        "return string representation of the Play"
        sorted_players = sorted(self.players,
                                key=lambda p: p.score,
                                reverse=True)

        return "%s: %s %s" % (self.date,
                              self.game,
                              ', '.join(['%s(%s)' % (player.name, player.score)
                                         for player in sorted_players]))

    def __load_json(self, json_data):
        "loads json datas"
        self.date = json_data['date']
        self.game = json_data['game']
        self.players = []
        self.type = 'max'
        self.winners = None
        for player_json in json_data['players']:
            self.players.append(Player(player_json))
        if 'winners' in json_data:
            self.winners = json_data['winners']

    def to_json(self):
        "serialize to json"
        if isinstance(self, Play):
            json_data = {"__class__": "Play",
                         "date": self.date,
                         "game": self.game}
            if hasattr(self, 'winners') and self.winners is not None:
                json_data['winners'] = self.winners
            json_data['players'] = [player.to_json()
                                    for player in self.players]
            return json_data
        raise TypeError(repr(self) + " cannot be serialized")

    def get_player_order(self):
        "return the list of player ordered per score"
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
        "return the winners of a play"
        if self.winners is not None:
            return self.winners
        return self.get_player_order()[0]


class Player(object):
    """docstring for Player"""
    def __init__(self, name='noname', score=0, json_data=None):
        super(Player, self).__init__()
        self.name = name
        self.score = score
        if json_data is not None:
            self.__load_json(json_data)

    def to_json(self):
        "serialize to json"
        if isinstance(self, Player):
            json_data = {"__class__": "Player",
                         "name": self.name,
                         "score": self.score}
            return json_data
        raise TypeError(repr(self) + " cannot be serialized")

    def __load_json(self, json_data):
        "loads json"
        self.name = json_data['name']
        self.score = json_data['score']

    def dummy(self):
        "dummy"
        pass


class OverallWinnerStat(object):
    """Gets the overall number of victory """
    def __init__(self):
        super(OverallWinnerStat, self).__init__()
        self.victory_per_player = {}

    def parse(self, scores):
        "parse given scores"
        for play in scores.plays:
            self.new_play(play)

    def new_play(self, play):
        "handle a new play in this stat"
        for winner in play.get_winners():
            print winner
            if winner not in self.victory_per_player:
                self.victory_per_player[winner] = 0
            self.victory_per_player[winner] = (1 +
                                               self.victory_per_player[winner])

    @staticmethod
    def description():
        "return the stat header"
        return "# Overall victories"

    def __str__(self):
        "to string !"
        result = ''
        for item in sorted(self.victory_per_player.items(),
                           key=lambda x: x[1]):
            result = result + '%s(%s)' % item

if __name__ == '__main__':
    MSCORES = Scores(filename='scores.json')
    STATS = OverallWinnerStat()
    STATS.parse(MSCORES)
    print STATS
