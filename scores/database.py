#!/usr/bin/env python
# encoding: utf-8

"""
The database connection management
"""
from __future__ import print_function

import hashlib
from mongokit import Connection, Document
from users import User


class Database(object):
    """The database connection"""

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
        user['passwd'] = Database.hash_password(passwd)
        user.save()

    def delete_user(self, login):
        """Delete the user with the given login"""
        user = self.get_user(login=login)
        if user:
            user.delete()

    @staticmethod
    def hash_password(passwd):
        """hash the password
        similar to how MySQL hashes passwords with the password() function.
        """
        hash_password = hashlib.sha1(passwd.encode('utf-8')).digest()
        hash_password = hashlib.sha1(hash_password).hexdigest()
        hash_password = '*' + hash_password.upper()
        return hash_password

    def get_user(self, login):
        """Retrieve the user with given login or None"""
        return self.db.User.one({'login': login})
