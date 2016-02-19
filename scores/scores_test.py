#!/usr/bin/env python
# encoding: utf-8

"test scores.py"

import scores
from scores import Play, Player, GameStat, PlayerStat, OverallWinnerStat
import pytest
import os
import yaml
import shutil

if not os.path.exists('target'):
    os.makedirs('target')


def test_scores():
    " test the score class init"
    mscores = scores.Scores()
    assert mscores is not None
    assert len(mscores.plays) == 0
    mscores = scores.Scores(filename='scores.yml')
    assert mscores is not None
    assert len(mscores.plays) > 0
    mscores = scores.Scores()
    assert mscores is not None
    mscores.load(filename='scores.yml')
    assert len(mscores.plays) > 0
    for player in mscores.plays[0].players:
        print '%s' % player
    print 'scores is %s' % mscores


def test_scores_dump():
    "test the Scores serialization"
    mscores = scores.Scores(filename='scores.yml')
    assert mscores is not None
    mscores.dump(filename='target/new_scores.yml')
    mscores2 = scores.Scores()
    mscores2.load('target/new_scores.yml')
    assert len(mscores.plays) == len(mscores2.plays)
    for play1, play2 in zip(mscores.plays, mscores2.plays):
        assert play1.date == play2.date
        assert play1.game == play2.game


def test_scores_dump_yaml():
    "test the Scores serialization"
    mscores = scores.Scores(filename='scores.yml')
    assert mscores is not None
    mscores.dump(filename='target/new_scores.yml')


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
    assert loaded_play.get_winners() == [ 'lolo' ]

def test_play():
    "test the play class"
    myplay = get_play()
    order = myplay.get_player_order()
    assert len(order) == 3
    assert order == [(100, ['cent']), (10, ['dix']), (1, ['un'])]
    myplay = Play()
    myplay.players.append(Player('cent', 100))
    myplay.players.append(Player('cent2', 100))
    myplay.players.append(Player('un', 1))
    order = myplay.get_player_order()
    assert len(order) == 2
    assert order == [(100, ['cent', 'cent2']), (1, ['un'])]
    print 'play is %s' % myplay
    myplay = Play()
    myplay.winners = ['cent', 'un']
    assert myplay.get_winners() == ['cent', 'un'], "expected winners list"
    myplay.winners = 'not a list FFS'
    with pytest.raises(TypeError):
        myplay.get_winners()


def test_play_to_json():
    myplay = get_play()
    myplay.winners = ['cent', 'un']
    assert myplay.to_json() is not None


def get_play():
    myplay = Play()
    myplay.players.append(Player('cent', 100))
    myplay.players.append(Player('dix', 10))
    myplay.players.append(Player('un', 1))
    return myplay


def test_game_stat():
    "Test the game stat class"
    game_stats = GameStat('parade')
    new_play = Play()
    new_play.game = 'parade'
    new_play.type = 'min'
    new_play.date = '10/01/16'
    new_play.players.append(Player(name='p1', score=10))
    new_play.players.append(Player(name='p2', score=1))

    game_stats.new_play(new_play)
    assert game_stats.get_highest_score() == new_play
    assert game_stats.get_lowest_score() == new_play

    # add new play
    # lowest
    new_play2 = Play()
    new_play2.game = 'parade'
    new_play2.type = 'min'
    new_play2.date = '11/01/16'
    new_play2.players.append(Player(name='p1', score=12))
    new_play2.players.append(Player(name='p2', score=1))
    game_stats.new_play(new_play2)
    # highest
    new_play3 = Play()
    new_play3.game = 'parade'
    new_play3.type = 'min'
    new_play3.date = '12/01/16'
    new_play3.players.append(Player(name='p1', score=12))
    new_play3.players.append(Player(name='p2', score=0))
    game_stats.new_play(new_play3)
    print ('highest score dates expected %s but found %s ' %
           (new_play3.date, game_stats.get_highest_score().date))
    assert game_stats.get_highest_score() == new_play3
    assert game_stats.get_lowest_score() == new_play2

    # test average score !
    assert game_stats.get_average_score() == 36/6


def test_player_stat():
    player_stat = PlayerStat('test_player')
    assert player_stat
    assert player_stat.__str__() != ''
    assert player_stat.get_worst_ennemy() == ('none', 0)


def test_overall_winner_stat():
    overall_stat = OverallWinnerStat()
    mscores = scores.Scores(filename='scores.yml')
    for play in mscores.plays:
        overall_stat.new_play(play)

    assert overall_stat
    assert overall_stat.__str__() != ''
    overall_stat.to_html()
    if os.path.exists('target/anunexpectedfolder'):
        shutil.rmtree('target/anunexpectedfolder')
    overall_stat.to_html(filename='target/anunexpectedfolder/index.html')
