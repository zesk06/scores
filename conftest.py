#!/usr/bin/env python
# encoding: utf-8

"""Test shared fixtures"""

import os
import pytest
from scores.database import Database


def pytest_addoption(parser):
    """Add options"""
    parser.addoption('--selenium', action='store_true', dest='doselenium',
                     help='to run selenium tests, '
                          'require a localhost:8080 webserver to be launched')


@pytest.fixture()
def database():
    """Create and return the connection
    :rtype: database.Database"""
    database_uri = ''
    if 'TEST_DATABASE_URI' in os.environ:
        database_uri = os.environ['TEST_DATABASE_URI']
    my_db = Database(uri=database_uri)
    # add 'test' user if needed
    if my_db.get_user(login='test') is None:
        my_db.add_user(login='test', name='Test User',
                       passwd='test01', email='test@test.com')
    return my_db
