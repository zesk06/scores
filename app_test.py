#!/usr/bin/env python
# encoding: utf-8

"test scores.py"

import app
import shutil
import os

print 'This run once'
THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEST_DIR = os.path.join(THIS_DIR, 'target')
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)
shutil.copy(app.FILENAME, os.path.join(TEST_DIR, 'scores.yml'))
app.FILENAME = 'target/scores.yml'


class TRequest(object):
    """docstring for TRequest"""
    def __init__(self):
        super(TRequest, self).__init__()
        self.form = dict()


def test_index():
    "Test the index page"
    assert app.index()


def test_new():
    "Test the new page"
    assert app.new()


def test_add():
    "Test the index page"
    new_request = TRequest()
    new_request.form['date'] = '10/03/16'
    new_request.form['game'] = 'test_game'
    new_request.form['players'] = """zesk:100
lolo:120
"""
    app.request = new_request
    assert app.add()
    assert app.get_mscores().plays[-1].game == 'test_game'
    assert app.get_mscores().plays[-1].date == '10/03/16'


def test_remove():
    "Test the index page"
    assert app.remove(0)
