#!/usr/bin/env python
# encoding: utf-8

"""
    This wonderfull app permits to display boardgame scores and stats
"""
from __future__ import print_function

import argparse
import json
import os
import sys
import flask
import flask_login
from flask import Flask, jsonify, render_template, request

import scores.scores as scores
import scores.database as database
from mongokit.document import StructureError

THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class Config(object):
    """A configuration class"""
    DEBUG = False
    TESTING = False
    FILE_URI = os.path.join(THIS_DIR, 'scores.yml')
    DATABASE_URI = 'mongodb://<dbuser>:<dbpassword>@<instance>.mlab.com:<port>/<dbname>'
    if 'DATABASE_URI' in os.environ:
        DATABASE_URI = os.environ['DATABASE_URI']


class DevelopmentConfig(Config):
    """The dev configuration"""
    DEBUG = True


class TestConfig(Config):
    """The test config"""
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

app.database = None


def get_db():
    """Return the Database
    :rtype: scores.database.Database"""
    if app.database is None:
        print('connecting to %s' % app.config['DATABASE_URI'])
        app.database = database.Database(app.config['DATABASE_URI'])
    return app.database


@login_manager.user_loader
def user_loader(login_s):
    # retrieve user from database
    print('user_loader')
    db = get_db()
    user = db.get_user(login_s)
    return user


@login_manager.request_loader
def request_loader(mrequest):
    print('request loader')
    mlogin = mrequest.form.get('username')
    passwd = mrequest.form.get('pw')
    if mlogin and passwd:
        db = get_db()
        user = db.get_user(mlogin)
        if user:
            if not user.authenticate(passwd):
                print('wrong password for %s' % mlogin)
        else:
            print('user %s not found' % mlogin)
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

    login = request.form.get('username')
    password = request.form['pw']
    db = get_db()
    user = db.get_user(login)
    if user and user.authenticate(password):
        flask_login.login_user(user)
        flask.flash('Logged in successfully.')
        # what is the next page?
        next_url = flask.request.args.get('next')
        if not next_is_valid(next_url, authenticated=True):
            return flask.abort(400)
        return flask.redirect(next_url or flask.url_for('index'))
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
    print('index')
    mscores = get_mscores()
    stats = scores.OverallWinnerStat()
    stats.parse(mscores)
    print('rendering')
    return render_template('base.html', title=u'GAME STATS', stats=stats)


def get_mscores():
    "returns the mscores"
    return scores.Scores(database=get_db())


@app.route('/api/v1/is_logged', methods=["GET"])
def is_logged():
    """
    :return: {"logged": "true"} if user is logged
    """

    return jsonify({"logged": True, "user_id": flask_login.current_user.get_id()})


@app.route('/api/v1/plays', methods=["POST"])
@flask_login.login_required
def add_play():
    """Adds a new play"""
    if 'Logged in as: ' + flask_login.current_user.get_id():
        play_json = request.json
        if request.json is None and request.data:
            play_json = request.data
        if play_json:
            print('adding play with json: %s' % play_json)
            try:
                play_json['created_by'] = flask_login.current_user.id
                new_play = get_db().add_play_from_json(play_json)
                return jsonify(msg='added play %s' % new_play.id,
                               id=new_play.id,
                               data=new_play.to_json()), 201
            except StructureError, error:
                return jsonify('BAD JSON %s: %s' % (error, play_json)), 400
        else:
            return jsonify('Failed to find JSON data in your POST'), 404
    return jsonify('You must be logged in to add a play'), 401


@app.route('/api/v1/plays', methods=["GET"])
def get_plays():
    """
    : return: the plays
    """
    mscores = get_mscores()
    return jsonify([json.loads(play.to_json()) for play in mscores.plays])


@app.route('/api/v1/plays/<play_id>', methods=["GET"])
def get_play(play_id):
    """
    : return: the play with given ID
    """
    mscores = get_mscores()
    play = mscores.get_play(play_id)
    if play:
        return jsonify(json.loads(play.to_json()))
    return jsonify('Failed to find play with id %s' % play_id), 404


@app.route('/api/v1/plays/<play_id>/elos', methods=["GET"])
def get_play_elos(play_id):
    """
    : return: the elos of the play with given ID
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    elos_per_player = stats.elo_stats.get_elos_per_player(play_id)
    if elos_per_player:
        json_object = []
        for player_login, elos in elos_per_player.iteritems():
            json_object.append({
                "login": player_login,
                "elo_before": elos[0],
                "elo_after": elos[1],
                "elos": elos[1] - elos[0],
            })
        return jsonify(json_object)
    return jsonify('Failed to find elos of play with id %s' % play_id), 404


@app.route('/api/v1/plays/<play_id>', methods=["DELETE"])
@flask_login.login_required
def delete_play(play_id):
    """
    Delete the play with the given id
    :param play_id: The id of the play to delete
    """
    mscores = get_mscores()
    play = mscores.get_play(play_id)
    if play:
        play.delete()
        return jsonify(msg='play deleted id %s' % play_id, data=play.to_json()), 200
    return jsonify('Failed to find play with id %s' % play_id), 404


@app.route('/api/v1/games', methods=["GET"])
def get_games():
    """Return the list of games"""
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    return jsonify(sorted(list(stats.game_stats)))


@app.route('/api/v1/games/<string:game_id>', methods=["GET"])
def get_game(game_id):
    """
    : return: the game with given ID
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    if game_id in stats.game_stats:
        return jsonify(stats.game_stats[game_id].to_json())
    return jsonify('Failed to find game %s' % game_id), 404


@app.route('/api/v1/players', methods=["GET"])
def get_players():
    """
    : return: Get all player stats
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    return jsonify([player_stat.to_json()
                    for player_stat in stats.player_stats.values()])


@app.route('/api/v1/players/<string:player_id>', methods=["GET"])
def get_player(player_id):
    """
    : return: the player with given ID
    """
    stats = scores.OverallWinnerStat()
    stats.parse(get_mscores())
    if player_id in stats.player_stats:
        return jsonify(stats.player_stats[player_id].to_json())
    return jsonify('Failed to find player with id %s' % player_id), 404


if __name__ == '__main__':
    parser = argparse.ArgumentParser('app.py')
    parser.add_argument('-d', help='goes in flask debug mode', action="store_true")
    parser.add_argument('port', help='The port, 5000 by default', nargs='?',
                        type=int, default=5000)
    args = parser.parse_args()

    print('launching server with args [%s]' % ', '.join(sys.argv))
    app.run(debug=args.d, port=args.port)
