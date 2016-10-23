#!/usr/bin/env python
# encoding: utf-8

"""
    The user management
"""

from mongokit import Document
from .common import hash_password


class User(Document):
    """
    A custom User
    extending UserMixin will permits to have basic auth methods
    extending Document makes this serializable in a database
    """

    def __init__(self, *args, **kwargs):
        # Document needs a lot of parameters
        Document.__init__(self, *args, **kwargs)
        self.authenticated = False

    __collection__ = 'users'
    structure = {
        'login': basestring,
        'name': basestring,
        'passwd': basestring,
        'email': basestring
    }

    required_fields = ['login', 'name', 'passwd']
    default_values = {
        'email': ''
    }

    # method required by flask_login
    # see flask_login.UserMixin
    @property
    def is_active(self):
        """Return true if user is active"""
        return True

    @property
    def is_authenticated(self):
        """Return True if user is authenticated"""
        return True

    def authenticate(self, passwd):
        """Try to authenticate with the given password
        :return: True if authentication was sucessfull
        :rtype: bool"""
        hpasswd = hash_password(passwd)
        self.authenticated = hpasswd == self['passwd']
        return self.authenticated

    @property
    def is_anonymous(self):
        """Anonymous user?"""
        return False

    def get_id(self):
        """return unique id"""
        return self['login']

    def login(self):
        """Return the user's name'"""
        return self['login']

    def name(self):
        """Return the user's name"""
        return self['name']
