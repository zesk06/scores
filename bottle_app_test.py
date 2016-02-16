#!/usr/bin/env python
# encoding: utf-8

"test scores.py"

import bottle_app
from bottle import Request
import shutil
import os

print 'This run once'
THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEST_DIR = os.path.join(THIS_DIR, 'target')
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)
shutil.copy(bottle_app.FILENAME, os.path.join(TEST_DIR, 'scores.yml'))
bottle_app.FILENAME = 'target/scores.yml'

class TRequest(object):
    """docstring for TRequest"""
    def __init__(self):
        super(TRequest, self).__init__()
        self.forms = dict()


def test_index():
    "Test the index page"
    assert bottle_app.index()


def test_new():
    "Test the index page"
    assert bottle_app.new()


def test_add():
    "Test the index page"
    newRequest = TRequest()
    newRequest.forms['date'] = '10/03/16'
    newRequest.forms['game'] = 'test_game'
    newRequest.forms['players'] = """zesk:100
lolo:120
"""
    bottle_app.request = newRequest
    assert bottle_app.add()
    assert bottle_app.get_mscores().plays[-1].game == 'test_game'
    assert bottle_app.get_mscores().plays[-1].date == '10/03/16'


def test_remove():
    "Test the index page"
    assert bottle_app.remove(0)

