#!/usr/bin/env python
# encoding: utf-8

"Handles scores"

import logging
import os

import yaml


THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEMPLATE_DIR = os.path.join(THIS_DIR, '..', 'templates')


LOGGER = logging.getLogger(__name__)


class Scores(object):
    """docstring for Scores"""

    def __init__(self, database=None):
        """Init
        :type database: Database
        """
        super(Scores, self).__init__()
        self.plays = []
        self.database = None
        if database is not None:
            self.database = database
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
        """Return the play with the given id
        :rtype: Play
        """
        for play in self.plays:
            if play.id == play_id:
                return play

    def add_play(self, play):
        """Add a new Play.
        :type play: Play
        :rtype: void
        """
        self.plays.append(play)
