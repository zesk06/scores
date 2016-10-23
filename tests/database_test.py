#!/usr/bin/env python
# encoding: utf-8

from scores.database import Database
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
