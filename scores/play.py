#!/usr/bin/env python
# encoding: utf-8

"""
    The Play management
"""

from mongokit import Document, CustomType
import datetime
import json

class Play(Document):
    """
    A database Play
    """

    def __init__(self, *args, **kwargs):
        # Document needs a lot of parameters
        Document.__init__(self, *args, **kwargs)
    # with this you will be able to use
    #  play.date = blah
    # play.players = blah2
    use_dot_notation = True
    __collection__ = 'plays'
    structure = {
        'date': datetime.datetime,
        'game': basestring,
        'winners': [basestring],
        'wintype': basestring,
        'players': [
            {
                'login': basestring,
                'score': int,
                'role': basestring,
                'color': basestring,
                'team': basestring,
                'team_color': basestring
            }
        ]
    }
    required_fields = ['date', 'game']
    default_values = {
        'winners': [],
        'players': [],
        'wintype': 'max'
    }

    def set_date(self, date):
        """Set the date
        :type date: datetime.datetime"""
        self['date'] = date

    def set_game(self, game):
        """Set the game
        :type game: basestring"""
        self['game'] = game

    def add_player(self, player_dict):
        """Adds a new player to the play
        :type player_dict: dict
         {
             'login': basestring,
             'score': int,
             'role': basestring,
             'color': basestring,
             'team': basestring,
             'team_color': basestring
         }
        """
        self['players'].append(player_dict)

    @staticmethod
    def create_player(login, score):
        """Return a player instance
        suitable to be added using the add_player method
        :rtype: dict"""
        return {
            'login': login,
            'score': score,
            'role': None,
            'color': None,
            'team': None,
            'team_color': None
        }

    def get_player_order(self):
        "return a list of tuple [(score, [players])] ordered per score"
        player_per_score = {}
        for (player, score) in [(player['login'], player['score'])
                                for player in self['players']]:
            if score not in player_per_score:
                player_per_score[score] = []
            player_per_score[score].append(player)
        if hasattr(self, 'type') and self['type'] == 'min':
            return sorted(player_per_score.items(), key=lambda x: x[0])
        return sorted(player_per_score.items(),
                      key=lambda x: x[0], reverse=True)

    def get_winners(self):
        "return the list of player names that wins the play"
        if self['winners'] is not None and isinstance(self['winners'], list):
            return self['winners']
        elif self['winners'] is not None:
            raise TypeError('Expected type for winners is list but found %s' %
                            type(self['winners']))
        return self.get_player_order()[0][1]

    def get_highest_score(self):
        "return the high score of the play"
        return self.get_player_order()[0][0]

    def get_lowest_score(self):
        "return the lowest score of the play"
        return self.get_player_order()[-1][0]

    @property
    def id(self):
        """return the id"""
        return '%s' % self['_id']
