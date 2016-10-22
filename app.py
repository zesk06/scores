#!/usr/bin/env python
# encoding: utf-8

"""
    This wonderfull app permits to display boardgame scores and stats
"""
from __future__ import print_function
import scores.scores as scores
import scores.users as users

import json
import os
import sys

import flask
import flask_login
from flask import Flask, jsonify, render_template, request

THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class Config(object):
    DEBUG = False
    TESTING = False
    FILE_URI = os.path.join(THIS_DIR, 'scores.yml')
    DATABASE_URI = 'mongodb://<dbuser>:<dbpassword>@<instance>.mlab.com:<port>/<dbname>'
    if 'DATABASE_URI' in os.environ:
        DATABASE_URI = os.environ['DATABASE_URI']


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    FILE_URI = os.path.join(THIS_DIR, 'target/scores.yml')
    DATABASE_URI = 'mongodb://<dbuser>:<dbpassword>@<instance>.mlab.com:<port>/<dbname>_test'
    if 'TEST_DATABASE_URI' in os.environ:
        DATABASE_URI = os.environ['TEST_DATABASE_URI']


app = Flask(__name__)
app.config.from_object(Config)

# used by flask-login
app.secret_key = 'idontwanttobeinthepubliccode'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(email):
    # if email not in MOCK_USERS:
    #     return
    user = User(email)
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('username')
    # if email not in MOCK_USERS:
    #     return
    # user = User(email)
    user.id = email
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == MOCK_USERS[email]['pw']
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = flask.request.form['username']
    password = flask.request.form['pw']
    # if email in MOCK_USERS and password == MOCK_USERS[email]['pw']:
    #     user = User(email)
    #     user.id = email
    #     flask_login.login_user(user)
    #     flask.flash('Logged in successfully.')
    #     # what is the next page?
    #     next_url = flask.request.args.get('next')
    #     if not next_is_valid(next_url, authenticated=True):
    #         return flask.abort(400)

    #     return flask.redirect(next_url or flask.url_for('index'))

    return 'Bad login'


def next_is_valid(url, authenticated):
    """Return True if next page is valid
    """
    protected_urls = ('protected', )
    if url in protected_urls and not authenticated:
        return False
    return True


@app.route('/logout')
def logout():
    """To logout from the web app"""
    flask_login.logout_user()
    flask.flash('Logged out successfully.')
    # what is the next page?
    next_url = flask.request.args.get('next')
    if not next_is_valid(next_url, False):
        return flask.abort(400)

    return flask.redirect(next_url or flask.url_for('index'))


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/')
def index():
    mscores = get_mscores()
    stats = scores.OverallWinnerStat()
    stats.parse(mscores)
    return render_template('base.html', title=u'GAME STATS', stats=stats)


def get_mscores():
    "returns the mscores"
    return scores.Scores(filename=app.config['FILE_URI'])


@app.route('/api/v1/is_logged', methods=["GET"])
def is_logged():
    """
    :return: {"logged": "true"} if user is logged
    """

    return jsonify({"logged": True, "user_id": flask_login.current_user.name})


@app.route('/api/v1/plays', methods=["GET"])
def get_plays():
    """
    :return: the plays
    """
    mscores = get_mscores()
    return jsonify([play.to_json() for play in mscores.plays])


@app.route('/api/v1/plays/<int:play_id>', methods=["GET"])
def get_play(play_id):
    """
    :return: the play with given ID
    """
    mscores = get_mscores()
    return jsonify(mscores.plays[play_id].to_json())


@app.route('/api/v1/games/<string:game_id>', methods=["GET"])
def get_game(game_id):
    """
    :return: the game with given ID
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    if game_id in stats.game_stats:
        return jsonify(stats.game_stats[game_id].to_json())
    return jsonify('Failed to find game %s' % game_id), 404


@app.route('/api/v1/players', methods=["GET"])
def get_players():
    """
    :return: Get all player stats
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    return jsonify([player_stat.to_json()
                    for player_stat in stats.player_stats.values()])


@app.route('/api/v1/players/<string:player_id>', methods=["GET"])
def get_player(player_id):
    """
    :return: the player with given ID
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    if player_id in stats.player_stats:
        return jsonify(stats.player_stats[player_id].to_json())
    return jsonify('Failed to find player with id %s' % player_id), 404


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    print('launching server with args [%s]' % ', '.join(sys.argv))
    app.run(debug=True, port=port)
