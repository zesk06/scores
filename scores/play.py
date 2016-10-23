#!/usr/bin/env python
# encoding: utf-8

"""
    The Play management
"""

from mongokit import Document, CustomType
import datetime


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
