#!/usr/bin/env python
# encoding: utf-8

"This bottle app permits to display boardgame scores"

from flask import Flask, request, jsonify, render_template
from jinja2 import Environment
from jinja2.loaders import PackageLoader
import os
import sys

import scores

THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.path.join(THIS_DIR, 'scores.yml')


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    DATABASE_URI = os.path.join(THIS_DIR, 'target/scores.yml')


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/test')
def test_page():
    return render_template('test.html')


@app.route('/')
def index():
    "return the homepage"
    mscores = get_mscores()
    stats = scores.OverallWinnerStat()
    stats.parse(mscores)
    menv = Environment(loader=PackageLoader('scores', 'templates'))
    template = menv.get_template('index.html')
    return template.render(title=u'GAME STATS', stats=stats)


@app.route('/new')
def new():
    " the page to create a new play record"
    menv = Environment(loader=PackageLoader('scores', 'templates'))
    template = menv.get_template('new.html')
    mscores = get_mscores()
    games = mscores.get_games()
    players = mscores.get_players()
    return template.render(title=u'NEW GAME', games=games, players=players)


@app.route('/add', methods=['POST'])
def add():
    " when posting for a new play record"
    mscores = get_mscores()
    new_play = scores.Play()
    new_play.date = request.form['date'].encode('utf-8')
    new_play.game = request.form['game'].encode('utf-8')
    players = request.form['players'].encode('utf-8')
    for player in [line for line in players.split('\n')
                   if len(line.rstrip()) > 0]:
        elements = player.split(':')
        if len(elements) == 2:
            (player_name, player_score) = elements
        else:
            return (('bad format for player line "%s", ' +
                     'shall contains 2 ":" separated tokens')
                    % player)
        new_player = scores.Player(name=player_name, score=player_score)
        new_play.players.append(new_player)
    if 'minmax' in request.form \
            and request.form['minmax'] \
            and len(request.form['minmax']) > 0:
            new_play.type = request.form['minmax']
    mscores.plays.append(new_play)
    mscores.dump(os.path.join(THIS_DIR, FILENAME))
    html = '<p>[<a href="/">OK</a>]: added play %s</p>' % new_play
    return html


# @get('/rm/<play_id:int>')
def remove(play_id):
    """
    remove the play record at index play_id
    :param play_id: The play id to be removed
    :return:
    """
    mscores = get_mscores()
    old_play = mscores.plays.pop(play_id)
    mscores.dump(app.config['DATABASE_URI'])
    return '<p>[<a href="/">OK</a>]: play %s has been removed</p>' % old_play


def get_mscores():
    "returns the mscores"
    return scores.Scores(filename=app.config['DATABASE_URI'])


@app.route('/api/v1/plays', methods=["GET"])
def get_plays():
    """
    :return: the plays
    """
    mscores = get_mscores()
    return jsonify([play.to_json() for play in mscores.plays])


@app.route('/api/v1/plays', methods=["POST"])
def add_play():
    """
    :return: Adds a new play
    """
    json_data = request.get_json(force=True)
    if json_data:
        new_play = scores.Play()
        new_play.from_json(data=json_data)
        get_mscores().add_play(play=new_play)
        return jsonify(new_play.to_json()), 201
    else:
        return jsonify('missing json data'), 400

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(debug=True, port=port)
