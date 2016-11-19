#!/usr/bin/env python
# encoding: utf-8

"test scores.py"
from __future__ import print_function
import datetime
import json
import os
import pytest
import time

import app
import scores.common as common

# This run once for all
THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEST_DIR = os.path.join(THIS_DIR, 'target')
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)
app.app.config.from_object(app.TestConfig)


class TestApp(object):

    @pytest.fixture(autouse=True)
    def set_up_app(self):
        self.app = app.app.test_client()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            pw=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_index(self):
        "Test the index page"
        assert self.app.get('/')

    def test_get_plays(self):
        self.app.get('/api/v1/plays')

    def test_add_play(self):
        """Test."""
        # login dude
        plays_before = self.app.get('/api/v1/plays').data
        before_nb = len(json.loads(plays_before))
        print('Before there are %s plays' % before_nb)
        tstamp = common.datetime_to_timestamp(datetime.datetime.now())
        json_data = {
            'game': 'test_game',
            'date': tstamp,
            'comment': 'This is a comment',
            'players': [
                {'login': 'test_zesk', 'score': 100, 'team': None,
                    'color': None, 'role': None, 'team_color': None},
                {'login': 'test_lolo', 'score': 10, 'team': None,
                    'color': None, 'role': None, 'team_color': None},
            ],
            'winners_reason': [],
            'winners': [],
            'wintype': 'max'
        }
        # post without login? shall not be ok
        response = self.app.post('/api/v1/plays',
                                 data=json.dumps(json_data),
                                 content_type='application/json')
        assert response.status_code == 302

        # login
        self.login('test', 'test01')
        response = self.app.post('/api/v1/plays',
                                 data=json.dumps(json_data),
                                 content_type='application/json')

        plays_after = self.app.get('/api/v1/plays')
        assert plays_after.status_code == 200
        plays = plays_after.data
        after_nb = len(json.loads(plays))
        print('received %s plays' % after_nb)
        assert after_nb == before_nb + 1
