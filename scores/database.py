#!/usr/bin/env python
# encoding: utf-8

"""
The database connection management
"""
from __future__ import print_function

import datetime
import json
import logging
import os
import re
import subprocess
import tempfile

from mongokit import Connection

from .common import hash_password
from .play import Play, PlayMigration
from .users import User


class Database(object):
    """The database connection"""

    @staticmethod
    def get_db():
        """Return the database based on DATABASE_URI env var
        :rtype: Database
        """
        if 'DATABASE_URI' in os.environ:
            uri = os.environ['DATABASE_URI']
            return Database(uri=uri)
        raise EnvironmentError('DATABASE_URI environment variable is missing')

    def __init__(self, uri):
        """Init the Database using given uri
        :param uri: The URI to connect to, such as
                    mongodb://LOGIN:PASSWORD@SERVER:PORT/DB_NAME
        """
        self.uri = uri
        self.connect(uri)
        self.dbname = uri.split('/')[-1]
        logging.info('dbname is %s', self.dbname)

    def connect(self, uri):
        """Connect to given uri
        :param uri: The URI to connect to, such as
                    mongodb://LOGIN:PASSWORD@SERVER:PORT/DB_NAME
        """
        logging.info('Connecting to uri %s', uri)
        self.connection = Connection(host=uri)
        self.connection.register([User, Play])
        return self.connection

    # pylint: disable=C0103
    @property
    def db(self):
        """Return the pymongo's db object using the database name"""
        return self.connection[self.dbname]

    def add_user(self, login, name, passwd, email):
        """Add a user
        :param login: The user login
        :param name: The user complete name
        :param passwd: The user password, will be hashed
        :param email: The user email"""
        # must not already exist
        if self.get_user(login=login):
            msg = 'A user with login "%s" has already been declared' % login
            raise ValueError(msg)
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

    # pylint: disable=R0201
    def authenticate_user(self, user, passwd):
        """Authenticate the user
        """
        hashed_passwd = hash_password(passwd)
        user.authauthenticate(hashed_passwd)

    def get_user(self, login):
        """Retrieve the user with given login or None"""
        return self.db.User.one({'login': login})

    def add_play(self, date, game, creator):
        """Add a play
        :type date: datetime.datetime
        :type game: basestring
        :rtype: Play"""
        play = self.db.Play()
        play.set_date(date)
        play.set_game(game)
        play.set_created_by(creator)
        play.save()
        return play

    def add_play_from_json(self, json_play):
        """Adds a play from a json definition
        :type json_play: dict|basestring
        :rtype: Play"""
        # TODO: improve typecheck
        if type(json_play) == dict:
            json_play = json.dumps(json_play)
        play = self.db.Play.from_json(json_play)
        play.save()
        return play

    def get_plays(self):
        """Return all plays"""
        return [play for play in self.db.Play.find()]

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
            os.rename(os.path.join(info['temp_folder'], info['db_name']),
                      dump_folder)
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
            self.drop()

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
        """Return configured UriInfo (host, port, username, password, dbname)
        based on the configured DATABASE_URI env var
        :rtype: tuple
        """
        if uri is None and 'DATABASE_URI' not in os.environ:
            msg = 'Must give uri or have os.environ[\'DATABASE_URI\']'
            raise RuntimeError(msg)
        elif uri is None:
            uri = os.environ['DATABASE_URI']

        return Database.parse_uri(uri)

    @staticmethod
    def parse_uri(uri):
        """Return the elements of the uri:
        (host, port, username, password, dbname)
        """
        match = re.match(
            (r'mongodb://(?P<user>[^:]+):(?P<password>[^@]+)'
             r'@(?P<host>[^:]+):(?P<port>\d+)/(?P<db_name>\w+)'), uri)
        if match:
            return {
                'host': match.group('host'),
                'port': match.group('port'),
                'user': match.group('user'),
                'password': match.group('password'),
                'db_name': match.group('db_name')
            }
        raise RuntimeError('Failed to parse uri: {}'.format(uri))
