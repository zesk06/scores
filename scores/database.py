#!/usr/bin/env python
# encoding: utf-8

"""
The database connection management
"""
from __future__ import print_function

import datetime
import hashlib
import logging
from mongokit import Connection, Document
import os
import re
import shutil
import subprocess
import tempfile
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
        self.uri = uri
        self.connect(uri)
        self.dbname = uri.split('/')[-1]
        print('dbname is %s' % self.dbname)

    def connect(self, uri):
        """Connect"""
        logging.info('Connecting to uri %s' % uri)
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

    def drop(self):
        """Drop the database"""
        self.connection.drop_database(self.dbname)

    def authenticate_user(self, user, passwd):
        hashed_passwd = hash_password(passwd)
        user.authauthenticate(hashed_passwd)

    def get_user(self, login):
        """Retrieve the user with given login or None"""
        return self.db.User.one({'login': login})

    def add_play(self, date, game):
        """Add a play
        :type date: datetime.datetime
        :type game: basestring
        :rtype: Play"""
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

    def dump(self, dump_folder=None):
        """Dump the database in the given dump_file
            Use the archive option to compress
            if uri is None, will use DATABASE_URI env var
            if dump_folder is None, will use a timetagged folder"""
        logging.info('mongodumping')
        info = Database.get_uri_info(uri=self.uri)

        if dump_folder is None:
            timetag = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
            dump_foldername = '{}_{}'.format(timetag, info['db_name'])
            dump_folder = os.path.join('dump', dump_foldername)
        info['dump_folder'] = dump_folder
        info['temp_folder'] = tempfile.mkdtemp()
        logging.info('mongodump on %s', info)
        cmd = '' \
            'mongodump -h {host} --port {port} -u {user} -p {password}' \
            ' --db {db_name} --out={temp_folder}'.format(**info)
        logging.info(cmd)
        if dump_folder != '' and not os.path.exists(dump_folder):
            os.makedirs(dump_folder)
        rcode = subprocess.call(cmd.split(' '))
        if rcode == 0:
            logging.info('dumped to %s', dump_folder)
            os.rename(os.path.join(info['temp_folder'], info['db_name']), dump_folder)
        else:
            logging.fatal('Failed to dump! - return code is %s', rcode)

    def restore(self, dump_folder, delete=False):
        """Restore a dump saved using mongodump in the given database"""
        logging.info('mongorestoring')
        if not os.path.exists(dump_folder):
            raise RuntimeError('dump folder does not exist %s' % dump_folder)
        info = Database.get_uri_info(uri=self.uri)
        info['dump_folder'] = dump_folder
        logging.info('mongorestore on %s', info)

        if delete:
            database = self.drop()

        cmd = '' \
            'mongorestore -h {host} --port {port} -u {user} -p {password}' \
            ' --db {db_name} {dump_folder}'.format(**info)
        logging.info(cmd)
        rcode = subprocess.call(cmd.split(' '))
        if rcode == 0:
            logging.info('restored from %s', dump_folder)
        else:
            logging.fatal('Failed to restore! - return code is %s', rcode)

    @staticmethod
    def get_uri_info(uri):
        if uri is None and 'DATABASE_URI' not in os.environ:
            raise RuntimeError('Must give uri or have os.environ[\'DATABASE_URI\']')
        elif uri is None:
            uri = os.environ['DATABASE_URI']

        return Database.parse_uri(uri)

    @staticmethod
    def parse_uri(uri):
        """Return the elements of the uri:
        (host, port, username, password, dbname)
        """
        match = re.match(r'mongodb://([^:]+):([^@]+)@([^:]+):(\d+)/(\w+)', uri)
        if match:
            return {
                'host': match.group(3),
                'port': match.group(4),
                'user': match.group(1),
                'password': match.group(2),
                'db_name': match.group(5)
            }
        raise RuntimeError('Failed to parse uri: {}'.format(uri))
