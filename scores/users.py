#!/usr/bin/env python
# encoding: utf-8

import flask_login

MOCK_USERS = {
    u'zesk': {'pw': 'secret'}}


class User(flask_login.UserMixin):
    """A custom use with basic functions implementedin superclass"""

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        """Return the user's name'"""
        return self.__name
