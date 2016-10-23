#!/usr/bin/env python
# encoding: utf-8

"""
The database connection management
"""
from __future__ import print_function

import hashlib
from mongokit import Connection, Document
import os

from .common import hash_password
from .users import User


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
        self.connection.register([User])
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
