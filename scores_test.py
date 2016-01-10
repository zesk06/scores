#!/usr/bin/env python
# encoding: utf-8

"test scores.py"

import scores
from scores import Play, Player
import pytest
import os
import json

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
    for player in mscores.plays[0].players:
        print '%s' % player


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


def test_play_load():
    "test"
    json_data = """{
    "date" : "01/09/15",
    "game" : "7wonders",
    "players" : [
      { "name" : "lolo"     , "score":28} ,
      { "name" : "clemence" , "score":46} ,
      { "name" : "zesk"     , "score":43} ,
      { "name" : "severine" , "score":59} ,
      { "name" : "vincent"  , "score":47} ,
      { "name" : "yohann"   , "score":55}
    ]
    }"""
    mplay = Play(json.loads(json_data))
    assert len(mplay.players) == 6
    assert mplay.players[0].name == 'lolo'
    assert mplay.players[0].score == 28


def test_play():
    "test the play class"
    myplay = Play()
    myplay.players.append(Player('un', 100))
    myplay.players.append(Player('deux', 10))
    myplay.players.append(Player('trois', 1))
    order = myplay.get_player_order()
    assert len(order) == 3
    assert order == [(100, ['un']), (10, ['deux']), (1, ['trois'])]
    myplay = Play()
    myplay.players.append(Player('un', 100))
    myplay.players.append(Player('deux', 100))
    myplay.players.append(Player('trois', 1))
    order = myplay.get_player_order()
    assert len(order) == 2
    assert order == [(100, ['un', 'deux']), (1, ['trois'])]

if __name__ == '__main__':
    pytest.main()
