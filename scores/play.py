#!/usr/bin/env python
# encoding: utf-8

"""
    The Play management
"""

import datetime

from mongokit import Document, DocumentMigration


class PlayMigration(DocumentMigration):
    """A DocumentMigration for the Play class"""

    def __init__(self, *args):
        DocumentMigration.__init__(self, *args)

    def allmigration01_add_comment(self):
        """Add the comment field to all"""
        self.target = {'comment': {'$exists': False}}  # pylint: disable=W0201
        self.update = {'$set': {'comment': None}}     # pylint: disable=W0201

    def allmigration02_add_reason(self):
        """Add the comment field to all"""
        self.target = {'winners_reason': {'$exists': False}}  # pylint: disable=W0201
        self.update = {'$set': {'winners_reason': []}}       # pylint: disable=W0201

    def allmigration03_add_created_by(self):
        """Add the created_by play field"""
        self.target = {'created_by': {'$exists': False}}  # pylint: disable=W0201
        self.update = {'$set': {'created_by': 'migration'}}       # pylint: disable=W0201


class Play(Document):
    """
    A database Play
    """

    def __init__(self, *args, **kwargs):
        # Document needs a lot of parameters
        Document.__init__(self, *args, **kwargs)
        # store the elo per player (before, after)
        self.elos_per_player = {}
    # with this you will be able to use
    #  play.date = blah
    # play.players = blah2
    use_dot_notation = True
    __collection__ = 'plays'
    structure = {
        'date': datetime.datetime,
        'game': basestring,
        'created_by': basestring,        # who created the play
        'winners': [basestring],         # a forced list of winners
        'winners_reason': [basestring],  # The forced list of winner reason
        'wintype': basestring,   # max or min
        'comment': basestring,   # A play comment
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

    def set_created_by(self, creator):
        """Set the created_by field
        :type creator: basestring"""
        self['created_by'] = creator

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
    def create_player(login, score, role=None, team=None):
        """Return a player instance
        suitable to be added using the add_player method
        :rtype: dict"""
        return {
            'login': login,
            'score': score,
            'role': role,
            'color': None,
            'team': team,
            'team_color': None
        }

    def get_player(self, login):
        """Return the player with the given login"""
        for player in self['players']:
            if player['login'] == login:
                return player
        raise ValueError('player with login %s not found' % login)

    def get_player_order(self):
        "return a list of tuple [(score, [players])] ordered per score"
        player_per_score = {}
        for (player, score) in [(player['login'], player['score'])
                                for player in self['players']]:
            if score not in player_per_score:
                player_per_score[score] = []
            player_per_score[score].append(player)
        if hasattr(self, 'wintype') and self['wintype'] == 'min':
            return sorted(player_per_score.items(), key=lambda x: x[0])
        return sorted(player_per_score.items(),
                      key=lambda x: x[0], reverse=True)

    def get_player_position(self, login):
        """Return the position of the player with the given login
        :type login: basestring
        :rtype: int
        """
        for index, score_players in enumerate(self.get_player_order()):
            players = score_players[1]
            if login in players:
                return index + 1
        raise ValueError('Player with login %s not found in play %s' % (login, self))

    def get_winners(self):
        "return the list of player names that wins the play"
        if self['winners'] is not None and \
           isinstance(self['winners'], list) and \
           self['winners'] != []:
            return self['winners']
        elif self['winners'] is not None and not isinstance(self['winners'], list):
            raise TypeError('Expected type for winners is list but found %s' %
                            type(self['winners']))
        order = self.get_player_order()
        if order != []:
            return self.get_player_order()[0][1]
        return []

    def get_highest_score(self):
        "return the high score of the play"
        order = self.get_player_order()
        if order != []:
            return order[0][0]
        return 0

    def get_lowest_score(self):
        "return the lowest score of the play"
        order = self.get_player_order()
        if order != []:
            return order[-1][0]
        return 0

    # pylint: disable=C0103
    @property
    def id(self):
        """return the id"""
        return '%s' % self['_id']

    @property
    def is_max(self):
        """Return True if play has a maxtype score"""
        return 'wintype' in self and self['wintype'] == 'max'

    @property
    def teams(self):
        """Return the map of teams
        { name: team_name, players: [...]}
        """
        teams = dict()
        for player in self.players:
            team = player['team']
            if team not in teams:
                teams[team] = []
            teams[team].append(player['login'])
        return teams

    def set_elos(self, elos_per_player):
        """Set the elos per player
        :param elos_per_player: The elos per player whre key is player login
                                and value is a tuple (elo_pre_play, elo_post_play)
        :type elos_per_player: dict(basestring, tuple(int,int))"""
        self.elos_per_player = elos_per_player
