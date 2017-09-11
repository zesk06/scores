#!/usr/bin/env python
# encoding: utf-8

# pylint tests exceptions:
# - R0201: method could be a function
# pylint: disable=R0201

""" A test module docstring"""

from __future__ import print_function

import datetime
import os
import tempfile

from scores.database import Database
from scores.play import Play


class TestDatabase(object):
    """ A Test class"""

    def test_uri(self, database):
        """Test the database uri field"""
        assert database.uri == os.environ['TEST_DATABASE_URI']

    def test_add_user(self, database):
        """
        :type database: database.Database"""
        if database.get_user('toto'):
            database.delete_user(login='toto')
        database.add_user('toto', 'Toto Doe', 'password01', 'toto@gmail.com')
        user = database.get_user('toto')
        assert user['login'] == 'toto'
        database.delete_user('toto')

    def test_play_crud(self, database):
        """Test the play CRUD
        :type play: scores.dadatabase.Database"""
        for play in database.get_plays():
            play.delete()
        created_by = 'test'
        new_play = database.add_play(datetime.datetime.now(), 'test_game', created_by)
        new_player = Play.create_player('login1', 1)
        new_play.add_player(new_player)
        new_player = Play.create_player('login2', 2)
        new_play.add_player(new_player)
        new_play.save()

        assert len(database.get_plays()) == 1

    def test_dump_delete_restore(self, database):
        """Test.
        :type database: scores.database.database"""
        database.drop()
        assert database.get_plays() == []
        # insert something
        created_by = 'test'
        database.add_play(datetime.datetime.now(), 'test_game1', created_by)
        database.add_play(datetime.datetime.now(), 'test_game2', created_by)
        assert len(database.get_plays()) == 2
        dump_folder = tempfile.mkdtemp()

        print('dump_folder is %s' % dump_folder)
        database.dump(dump_folder=dump_folder)
        assert os.path.exists(dump_folder)
        # insert a third item, that will be erased by the restore
        database.add_play(datetime.datetime.now(), 'test_game3', created_by)
        assert len(database.get_plays()) == 3

        database.restore(dump_folder=dump_folder, delete=True)
        assert len(database.get_plays()) == 2

    def test_parse_uri(self):
        """A test"""
        tests = (
            ('mongodb://heroku:herokuPASSWORD@my.host.mlab.com:12345/my_db_name',
             ('my.host.mlab.com',
              '12345',
              'heroku',
              'herokuPASSWORD',
              'my_db_name')),
            ('mongodb://user:password@host:12345/db_name',
             ('host',
              '12345',
              'user',
              'password',
              'db_name'))
        )
        for test in tests:
            uri = test[0]
            resp = test[1]
            assert Database.parse_uri(uri) == {
                'host': resp[0],
                'port': resp[1],
                'user': resp[2],
                'password': resp[3],
                'db_name': resp[4]
            }

    def test_add_play_from_json(self, database):
        """A test"""
        created_by = 'test'
        new_play = database.add_play(datetime.datetime.now(), 'test_game', created_by)
        print('New play is %s' % new_play.to_json())
        database.add_play_from_json(new_play.to_json())
