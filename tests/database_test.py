#!/usr/bin/env python
# encoding: utf-8

from scores.database import Database
from scores.play import Play

import datetime
import pytest
import os


class TestDatabase(object):
    """ A Test class"""

    @pytest.fixture()
    def database(self):
        """Create and return the connection"""
        database_uri = ''
        if 'TEST_DATABASE_URI' in os.environ:
            database_uri = os.environ['TEST_DATABASE_URI']
        return Database(uri=database_uri)

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

        new_play = database.add_play(datetime.datetime.now(), 'test_game')
        new_player = Play.create_player('login1', 1)
        new_play.add_player(new_player)
        new_player = Play.create_player('login2', 2)
        new_play.add_player(new_player)
        new_play.save()

        assert len(database.get_plays()) == 1
