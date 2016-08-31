#!/usr/bin/env python
# encoding: utf-8

"test scores.py"

import json
import shutil
import os

import app

# This run once for all
THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
TEST_DIR = os.path.join(THIS_DIR, 'target')
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)
shutil.copy(os.path.join(THIS_DIR, 'scores.yml'),
            os.path.join(TEST_DIR, 'scores.yml'))
app.app.config.from_object(app.TestConfig)


class AppTest(object):

    def test_index(self):
        "Test the index page"
        assert app.index(self)

    def test_get_plays(self):
        with app.app.test_client() as myapp:
            myapp.get('/api/v1/plays')

    def test_add_play(self):
        """Test."""
        with app.app.test_client() as myapp:
            plays_before = myapp.get('/api/v1/plays')
            json_data = {
                'game': 'test_game',
                'date': '10/03/16',
                'players': [
                    {'name': 'test_zesk', 'score': 100, 'team': None},
                    {'name': 'test_lolo', 'score': 10, 'team': None}
                ]
            }
            myapp.post(data=json.dumps(json_data),
                       content_type='application/json')
            plays_after = myapp.get('/api/v1/plays')
            assert plays_after.status_code == 200
            plays = plays_after.data
            print 'received %s plays' % len(json.loads(plays))
