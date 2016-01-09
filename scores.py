#!/usr/bin/env python
# encoding: utf-8

"Handles scores"

import json


class Scores(object):
    """docstring for Scores"""
    def __init__(self, json_data):
        super(Scores, self).__init__()
        self.plays = []
        for json_play in json_data:
            self.plays.append(Play(json_play))

    def __str__(self):
        "returns string representation"
        return "%s" % '\n'.join([str(play) for play in self.plays])


class Play(object):
    """docstring for ClassName"""
    def __init__(self, json_data):
        super(Play, self).__init__()
        self.date = json_data['date']
        self.game = json_data['game']
        self.players = []
        for player_json in json_data['players']:
            self.players.append(Player(player_json))

    def __str__(self):
        "return string representation of the Play"
        sorted_players = sorted(self.players,
                                key=lambda p: p.score,
                                reverse=True)

        return "%s: %s %s" % (self.date,
                              self.game,
                              ', '.join(['%s(%s)' % (player.name, player.score)
                                         for player in sorted_players]))


class Player(object):
    """docstring for Player"""
    def __init__(self, json_data):
        super(Player, self).__init__()
        self.name = json_data['name']
        self.score = json_data['score']


def load(filename='scores.json'):
    with open(filename) as json_file:
        json_data = json.load(json_file)
        scores = Scores(json_data)
        print scores


if __name__ == '__main__':
    load()
