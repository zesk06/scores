#!/usr/bin/env python
# encoding: utf-8

"test scores.py"

import scores
from scores import Play, Player
import pytest
import os


if not os.path.exists('target'):
    os.makedirs('target')


def test_scores():
    " test the score class init"
    mscores = scores.Scores()
    assert mscores is not None
    assert len(mscores.plays) == 0
    mscores = scores.Scores(filename='scores.json')
    assert mscores is not None
    assert len(mscores.plays) > 0
    mscores = scores.Scores()
    assert mscores is not None
    mscores.load(filename='scores.json')
    assert len(mscores.plays) > 0


def test_scores_dump():
    "test the Scores serialization"
    mscores = scores.Scores(filename='scores.json')
    assert mscores is not None
    mscores.dump(filename='target/new_scores.json')
    mscores2 = scores.Scores()
    mscores2.load('target/new_scores.json')
    assert len(mscores.plays) == len(mscores2.plays)
    for play1, play2 in zip(mscores.plays, mscores2.plays):
        assert play1.date == play2.date
        assert play1.game == play2.game


def test_play():
    "test the play class"
    myplay = Play()
    myplay.players.append(Player('un', 100))
    myplay.players.append(Player('deux', 10))
    myplay.players.append(Player('trois', 1))
    order = myplay.get_player_order()
    assert len(order) == 3
    assert order == [(100, ['un']), (10, ['deux']), (1, ['trois'])]

if __name__ == '__main__':
    pytest.main()
