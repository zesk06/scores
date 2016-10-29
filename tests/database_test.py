#!/usr/bin/env python
# encoding: utf-8

from scores.database import Database
from scores.play import Play

import datetime
import pytest
import os


class TestDatabase():

    @pytest.fixture()
    def db(self):
        """Create and return the connection"""
        if 'TEST_DATABASE_URI' in os.environ:
            database_uri = os.environ['TEST_DATABASE_URI']
        return Database(uri=database_uri)

    def test_add_user(self, db):
        """
        :type db: database.Database"""
        if db.get_user('toto'):
            db.delete_user(login='toto')
        db.add_user('toto', 'Toto Doe', 'password01', 'toto@gmail.com')
        user = db.get_user('toto')
        assert user['login'] == 'toto'
        db.delete_user('toto')

    def test_play_crud(self, db):
        """Test the play CRUD
        :type play: scores.dadatabase.Database"""
        for play in db.get_plays():
            play.delete()

        new_play = db.add_play(datetime.datetime.now(), 'test_game')
        new_player = Play.get_player('login1', 1)
        new_play.add_player(new_player)
        new_player = Play.get_player('login2', 2)
        new_play.add_player(new_player)
        new_play.save()

        assert len(db.get_plays()) == 1


