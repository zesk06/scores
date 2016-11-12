#!/usr/bin/env python
# encoding: utf-8

"""
The database connection management
"""
from __future__ import print_function

import datetime
import hashlib
from mongokit import Connection, Document
import os
import yaml

from .common import hash_password
from .users import User
from .play import Play, PlayMigration


class Database(object):
    """The database connection"""

    @staticmethod
    def get_db():
        if 'DATABASE_URI' in os.environ:
            uri = os.environ['DATABASE_URI']
            return Database(uri=uri)
        raise EnvironmentError('DATABASE_URI environment variable is missing')

    def __init__(self, uri):
        """Init"""
        self.connect(uri)
        self.dbname = uri.split('/')[-1]
        print('dbname is %s' % self.dbname)

    def connect(self, uri):
        """Connect"""
        self.connection = Connection(host=uri)
        self.connection.register([User, Play])
        return self.connection

    @property
    def db(self):
        """Return the pymongo's db object using the database name"""
        return self.connection[self.dbname]

    def add_user(self, login, name, passwd, email):
        """Add a user"""
        # must not already exist
        if self.get_user(login=login):
            raise ValueError(
                'A user with login "%s" has already been declared' % login)
        user = self.db.User()
        user['login'] = login
        user['name'] = name
        user['email'] = email
        user['passwd'] = hash_password(passwd)
        user.save()

    def delete_user(self, login):
        """Delete the user with the given login"""
        user = self.get_user(login=login)
        if user:
            user.delete()

    def authenticate_user(self, user, passwd):
        hashed_passwd = hash_password(passwd)
        user.authauthenticate(hashed_passwd)

    def get_user(self, login):
        """Retrieve the user with given login or None"""
        return self.db.User.one({'login': login})

    def add_play(self, date, game):
        """Add a play
        :type date: datetime.datetime"""
        play = self.db.Play()
        play.set_date(date)
        play.set_game(game)
        play.save()
        return play

    def get_plays(self):
        """Return all plays"""
        return [play for play in self.db.Play.find()]

    def from_yaml(self, yaml_file, save=False):
        """Imports plays from a yaml object
        :param yaml_file: The yaml file to import
        :param save: if True, will save the oject on the database, False will only validate"""
        with open(yaml_file) as yml_file:
            # loading yaml.safe_load ensure byte str instead of unicode string
            yml_data = yaml.safe_load(yml_file)
            for json_play in yml_data:
                new_play = self.db.Play()
                # date DD/MM/YYY to datetime ?
                # let's put the time 21:00
                new_play.date = datetime.datetime.strptime(json_play['date'], '%d/%m/%y')
                new_play.date = new_play.date.replace(hour=21, minute=00)
                new_play.game = json_play['game']
                if 'winners' in json_play:
                    new_play.winners = json_play['winners']
                if 'winners_reason' in json_play:
                    new_play.winners_reason = json_play['winners_reason']
                if 'type' in json_play:
                    new_play.wintype = json_play['type']
                if 'comment' in json_play:
                    new_play.comment = json_play['comment']
                for player_json in json_play['players']:
                    new_player = Play.create_player(
                        player_json['name'], player_json['score'])
                    if 'team' in player_json:
                        new_player['team'] = player_json['team']
                    if 'team_color' in player_json:
                        new_player['team_color'] = player_json['team_color']
                    if 'color' in player_json:
                        new_player['color'] = player_json['color']
                    if 'role' in player_json:
                        new_player['role'] = player_json['role']
                    new_play.add_player(new_player)
                if save:
                    new_play.save()
                    print('SAVED %s - %s' % (new_play.game, new_play.date))
                else:
                    new_play.validate()
                    print('VALID %s - %s' % (new_play.game, new_play.date))

    def migrate_all(self):
        """Runs the migration rules in bulk"""
        migration_play = PlayMigration(Play)
        migration_play.migrate_all(self.db.plays)  # pylint: disable=E1101
