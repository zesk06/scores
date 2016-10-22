#!/usr/bin/env python
# encoding: utf-8

"test scores.py"


from scores.scores import Play, Player, GameStat, PlayerStat, OverallWinnerStat, Scores
import pytest
import os
import yaml
import shutil


@pytest.fixture()
def test_dir():
    """
    :rtype: basestring
    :return: a suitable dir for testing outputs
    """
    if not os.path.exists('target'):
        os.makedirs('target')
    return 'target'


@pytest.fixture()
def mscores():
    """
    :return: a test instance of mscores
    """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    return Scores(filename=os.path.join(this_dir, '..', 'scores.yml'))


def test_scores(mscores):
    " test the score class init"
    assert len(Scores().plays) == 0
    assert mscores is not None
    assert len(mscores.plays) > 0


def test_scores_dump(mscores, test_dir):
    "test the Scores serialization"
    mscores.dump(filename=os.path.join(test_dir, 'new_scores.yml'))
    mscores2 = Scores()
    mscores2.load(os.path.join(test_dir, 'new_scores.yml'))
    assert len(mscores.plays) == len(mscores2.plays)
    for play1, play2 in zip(mscores.plays, mscores2.plays):
        assert play1.date == play2.date
        assert play1.game == play2.game


def test_scores_dump_yaml(mscores, test_dir):
    "test the Scores serialization"
    mscores.dump(filename=os.path.join(test_dir, 'new_scores.yml'))


def test_scores_get_games(mscores):
    """
    test the Scores.get_games method
    :param mscores: the mscores
    """
    assert len(mscores.get_games()) > 0


def test_play_load():
    "test"
    # yaml format?
    yaml_str = """
date: 15/01/16
game: parade
players:
- {name: allugan, score: 9}
- {name: clemence, score: 8}
- {name: jc, score: 11}
- {name: lolo, score: 9}
- {name: vincent, score: 19}
- {name: zesk, score: 12}
type: min
"""
    loaded_play = Play(yaml.load(yaml_str))
    assert len(loaded_play.players) == 6
    assert loaded_play.players[0].name == 'allugan'
    assert loaded_play.players[0].score == 9
    assert loaded_play.type == 'min'
    # yaml format?
    yaml_str = """
date: 15/01/16
game: splendor
winners:
- lolo
players:
- {name: lolo, score: 16}
- {name: maxime, score: 13}
- {name: zesk, score: 16}
"""
    loaded_play = Play(yaml.load(yaml_str))
    assert loaded_play.get_winners() == ['lolo']


def test_play():
    "test the play class"
    myplay = __get_play(players='cent=100,dix=10,un=1')
    order = myplay.get_player_order()
    assert len(order) == 3
    assert order == [(100, ['cent']), (10, ['dix']), (1, ['un'])]
    myplay = __get_play(players='cent=100,cent2=100,un=1')
    order = myplay.get_player_order()
    assert len(order) == 2
    assert order == [(100, ['cent', 'cent2']), (1, ['un'])]
    print 'play is %s' % myplay
    myplay = __get_play(players='', winners=['cent,un'])
    myplay.winners = ['cent', 'un']
    assert myplay.get_winners() == ['cent', 'un'], "expected winners list"
    myplay.winners = 'not a list FFS'
    with pytest.raises(TypeError):
        myplay.get_winners()


def test_play_to_json():
    """
    test play serialization
    """
    myplay = __get_play(players='cent=100,dix=10,un=1', winners=['cent', 'un'])
    assert myplay.to_json() is not None


def test_game_stat():
    "Test the game stat class"
    game_stats = GameStat('parade')
    new_play = __get_play(type='min', players='P1=10,p2=1', date='10/01/16')
    game_stats.new_play(new_play)
    assert game_stats.get_highest_score() == new_play
    assert game_stats.get_lowest_score() == new_play
    # add new play
    # lowest
    new_play2 = __get_play(type='min', players='P1=12,p2=1', date='11/01/16')
    game_stats.new_play(new_play2)
    # highest
    new_play3 = __get_play(type='min', players='P1=12,p2=0', date='12/01/16')
    game_stats.new_play(new_play3)
    print ('highest score dates expected %s but found %s ' %
           (new_play3.date, game_stats.get_highest_score().date))
    assert game_stats.get_highest_score() == new_play3
    assert game_stats.get_lowest_score() == new_play2
    # test average score !
    assert game_stats.get_average_score() == 36 / 6
    # test best player is p2
    assert game_stats.get_best_player() == 'p2'


def test_player_stat():
    player_stat = PlayerStat('test_player')
    assert player_stat
    assert player_stat.__str__() != ''
    assert player_stat.get_worst_ennemy() == ('none', 0)
    assert player_stat.last == 0
    # loss + last
    player_stat.new_play(__get_play(players='test_player=0,first=10'))
    # loss + not last
    player_stat.new_play(__get_play(players='test_player=5,other=10,last=0'))
    assert player_stat.last == 1


def __get_play(game='test_game',
               date='31/12/16',
               type='max', players='p1=12,p2=0',
               winners=None):
    """
    return a test play
    :param game:
    :param date:
    :param type:
    :param players:
    :return:
    """
    new_play = Play()
    new_play.game = game
    new_play.type = type
    new_play.date = date
    if players is None:
        new_play.players.append(Player(name='p1', score=12))
        new_play.players.append(Player(name='p2', score=0))
    elif len(players) > 0:
        for name, score in [player.split('=')
                            for player in players.split(',')]:
            new_play.players.append(Player(name, score))
    if winners:
        new_play.winners = winners
    return new_play


def test_player_stat_winloss_streak():
    """
    test the streaks of win or loose
    :return:
    """
    pstat = PlayerStat('test_player')
    assert pstat.streak_win == 0
    assert pstat.streak_loose == 0
    pstat._PlayerStat__new_win()
    assert pstat.streak_win == 1
    assert pstat.streak_win_longest == 1
    assert pstat.streak_loose == 0
    pstat._PlayerStat__new_win()
    assert pstat.streak_win == 2
    assert pstat.streak_win_longest == 2
    assert pstat.streak_loose == 0
    pstat._PlayerStat__new_loss(['other'])
    assert pstat.streak_win == 0
    assert pstat.streak_loose == 1
    assert pstat.streak_loose_longest == 1
    pstat._PlayerStat__new_loss(['other'])
    assert pstat.streak_win == 0
    assert pstat.streak_win_longest == 2
    assert pstat.streak_loose == 2
    assert pstat.streak_loose_longest == 2
    pstat._PlayerStat__new_win()
    assert pstat.streak_win == 1
    assert pstat.streak_win_longest == 2
    assert pstat.streak_loose == 0
    assert pstat.streak_loose_longest == 2
    pstat._PlayerStat__new_win()
    pstat._PlayerStat__new_win()
    pstat._PlayerStat__new_win()
    assert pstat.streak_win == 4
    assert pstat.streak_win_longest == 4


def test_overall_winner_stat(mscores, test_dir):
    overall_stat = OverallWinnerStat()
    for play in mscores.plays:
        overall_stat.new_play(play)

    assert overall_stat
    assert overall_stat.__str__() != ''
    overall_stat.to_html()
    if os.path.exists(os.path.join(test_dir, 'unexpected')):
        shutil.rmtree(os.path.join(test_dir, 'unexpected'))
    overall_stat.to_html(filename=os.path.join(test_dir,
                                               'unexpected/index.html'))
