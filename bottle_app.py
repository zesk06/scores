
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, request, route, post, get
from jinja2 import Environment
from jinja2.loaders import PackageLoader
import scores
import os

THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
MSCORES = scores.Scores(filename=os.path.join(THIS_DIR, 'scores.json'))

@route('/')
def index():
    STATS = scores.OverallWinnerStat()
    STATS.parse(MSCORES)
    return STATS.get_html()

@get('/new')
def new():
    " return the html"
    menv = Environment(loader=PackageLoader('scores', 'templates'))
    template = menv.get_template('new.html')
    return template.render(title=u'NEW GAME')

@post('/add')
def add():
    new_play = scores.Play()
    new_play.date = request.forms.get('date')
    new_play.game = request.forms.get('game')
    players = request.forms.get('players')
    for player in players.split(' '):
        (player_name,player_score) = player.split(':')
        new_player = scores.Player(name=player_name, score=player_score)
        new_play.players.append(new_player)
    MSCORES.plays.append(new_play)
    MSCORES.dump(os.path.join(THIS_DIR, 'scores.json'))
    return '<p>[<a href="/">OK</a>]: %s</p>' % new_play

@get('/rm/<play_id:int>')
def remove(play_id):
    old_play = MSCORES.plays.pop(play_id)
    MSCORES.dump(os.path.join(THIS_DIR, 'scores.json'))
    return '<p>[<a href="/">OK</a>]: play %s has been removed</p>' % old_play

application = default_app()

