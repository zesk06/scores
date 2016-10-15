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
    return render_template('base.html', title=u'GAME STATS', stats=stats)


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
