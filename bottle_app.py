
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route
import scores
import os

THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

@route('/')
def hello_world():
    MSCORES = scores.Scores(filename=os.path.join(THIS_DIR, 'scores.json'))
    STATS = scores.OverallWinnerStat()
    STATS.parse(MSCORES)
    return STATS.get_html()

application = default_app()

