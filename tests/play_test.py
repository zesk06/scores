#!/usr/bin/env python
# encoding: utf-8

"test scores.py"


from scores.scores import GameStat, PlayerStat, OverallWinnerStat, Scores
from scores.play import Play
from scores.database import Database
import pytest
import os
import yaml
import shutil
import uuid


class TestPlay(object):
    """ A Test class"""

    def test_play_load(self):
        "test"
        # yaml format?
        yaml_str = """
    created_by: py.test
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
        assert loaded_play.players[0]['name'] == 'allugan'
        assert loaded_play.players[0]['score'] == 9
        assert loaded_play['type'] == 'min'
        # yaml format?
        yaml_str = """
    created_by: py.test
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

    def test_play(self):
        "test the play class"
        myplay = self.__get_play(players='cent=100,dix=10,un=1')
        order = myplay.get_player_order()
        assert len(order) == 3
        assert order == [(100, ['cent']), (10, ['dix']), (1, ['un'])]
        myplay = self.__get_play(players='cent=100,cent2=100,un=1')
        order = myplay.get_player_order()
        assert len(order) == 2
        assert order == [(100, ['cent', 'cent2']), (1, ['un'])]
        print 'play is %s' % myplay
        myplay = self.__get_play(players='', winners=['cent,un'])
        myplay.winners = ['cent', 'un']
        assert myplay.get_winners() == ['cent', 'un'], "expected winners list"
        myplay.winners = 'not a list FFS'
        with pytest.raises(TypeError):
            myplay.get_winners()

    def test_get_player_position(self):
        """Test."""
        myplay = self.__get_play(players='cent=100,dix=10,un=1')
        assert myplay.get_player_position('cent') == 1
        assert myplay.get_player_position('dix') == 2
        assert myplay.get_player_position('un') == 3

        myplay = self.__get_play(players='cent=100,dix=10,un=1', wintype='min')
        assert myplay.get_player_position('cent') == 3
        assert myplay.get_player_position('dix') == 2
        assert myplay.get_player_position('un') == 1

        with pytest.raises(ValueError):
            myplay.get_player_position('i_dont_know_U')

    def __get_play(self, game='test_game',
                   date='31/12/16',
                   wintype='max', players='p1=12,p2=0',
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
        new_play.wintype = wintype
        new_play.date = date
        new_play['_id'] = uuid.uuid4()
        if players is None:
            new_play.players.append(Play.create_player(login='p1', score=12))
            new_play.players.append(Play.create_player(login='p1', score=12))
        elif len(players) > 0:
            for name, score in [player.split('=')
                                for player in players.split(',')]:
                new_play.players.append(Play.create_player(login=name, score=int(score)))
        if winners:
            new_play.winners = winners
        return new_play
