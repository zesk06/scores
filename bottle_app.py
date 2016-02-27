#!/usr/bin/env python
# encoding: utf-8
# A very simple Bottle Hello World app for you to get started with...

"This bottle app permits to display boardgame scores"

import bottle
from bottle import default_app, request, route, post, get, run
from bottle import static_file
from jinja2 import Environment
from jinja2.loaders import PackageLoader
import scores
import os


THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
FILENAME = os.path.join(THIS_DIR, 'scores.yml')


@route('/')
def index():
    "return the homepage"
    mscores = get_mscores()
    stats = scores.OverallWinnerStat()
    stats.parse(mscores)
    menv = Environment(loader=PackageLoader('scores', 'templates'))
    template = menv.get_template('index.html')
    return template.render(title=u'GAME STATS', stats=stats)


@get('/new')
def new():
    " the page to create a new play record"
    menv = Environment(loader=PackageLoader('scores', 'templates'))
    template = menv.get_template('new.html')
    return template.render(title=u'NEW GAME')


@post('/add')
def add():
    " when posting for a new play record"
    mscores = get_mscores()
    new_play = scores.Play()
    new_play.date = request.forms.get('date')
    new_play.game = request.forms.get('game')
    players = request.forms.get('players')
    for player in [line for line in players.split('\n') if len(line.rstrip()) > 0]:
        elements = player.split(':')
        if len(elements) == 2:
            (player_name, player_score) = elements
        else:
            return (('bad format for player line "%s", ' +
                     'shall contains 2 ":" separated tokens')
                    % player)
        new_player = scores.Player(name=player_name, score=player_score)
        new_play.players.append(new_player)
    if request.forms.get('minmax') and len(request.forms.get('minmax')) > 0:
        new_play.type = request.forms.get('minmax')
    mscores.plays.append(new_play)
    mscores.dump(os.path.join(THIS_DIR, FILENAME))
    html = '<p>[<a href="/">OK</a>]:'
    html += ('added play %s (minmax was %s)</p>' %
             (new_play, request.forms.get('minmax')))
    return html


@get('/rm/<play_id:int>')
def remove(play_id):
    """
    remove the play record at index play_id
    :param play_id: The play id to be removed
    :return:
    """
    mscores = get_mscores()
    old_play = mscores.plays.pop(play_id)
    mscores.dump(os.path.join(THIS_DIR, FILENAME))
    return '<p>[<a href="/">OK</a>]: play %s has been removed</p>' % old_play


@route('/static/<filename>')
def server_static(filename):
    """
    :return: static files
    """
    return static_file(filename, root=os.path.join(THIS_DIR, 'static'))


def get_mscores():
    "returns the mscores"
    return scores.Scores(filename=os.path.join(THIS_DIR, FILENAME))


application = default_app()  # pylint: disable = C0103

if __name__ == '__main__':
    bottle.debug(True)
    run(reloader=True)
