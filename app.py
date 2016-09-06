#!/usr/bin/env python
# encoding: utf-8

"This bottle app permits to display boardgame scores"

import json
import os
import sys

import scores
from flask import Flask, jsonify, render_template, request

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


@app.route('/')
def index_angular():
    mscores = get_mscores()
    stats = scores.OverallWinnerStat()
    stats.parse(mscores)
    return render_template('index.html', title=u'GAME STATS', stats=stats)


@app.route('/new')
def new():
    " the page to create a new play record"
    mscores = get_mscores()
    games = mscores.get_games()
    players = mscores.get_players()
    return render_template('new.html', title=u'NEW GAME',
                           games=games, players=players)


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


@app.route('/api/v1/plays/<int:play_id>', methods=["GET"])
def get_play(play_id):
    """
    :return: the play with given ID
    """
    mscores = get_mscores()
    return jsonify(mscores.plays[play_id].to_json())


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
    print('launching server with args [%s]' % ', '.join(sys.argv))
    app.run(port=port)
