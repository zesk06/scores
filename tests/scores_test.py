#!/usr/bin/env python
# encoding: utf-8

"test scores.py"


import os
import shutil
import uuid

import pytest
import yaml

from scores.database import Database
from scores.play import Play
from scores.scores import Scores
from scores.stats.stats_overall import OverallWinnerStat
from scores.stats.stats_game import StatsGame
from scores.stats.stats_player import StatsPlayer


class TestScores(object):
    """ A Test class"""

    @pytest.fixture()
    def test_dir(self):
        """
        :rtype: basestring
        :return: a suitable dir for testing outputs
        """
        if not os.path.exists('target'):
            os.makedirs('target')
        return 'target'

    @pytest.fixture()
    def database(self):
        """Create and return the connection"""
        if 'TEST_DATABASE_URI' in os.environ:
            database_uri = os.environ['TEST_DATABASE_URI']
        return Database(uri=database_uri)

    @pytest.fixture()
    def mscores(self, database):
        """
        :return: a test instance of mscores
        """
        return Scores(database=database)

    def test_scores(self, mscores):
        " test the score class init"
        assert len(Scores().plays) == 0
        assert mscores is not None
        assert len(mscores.plays) > 0

    def test_scores_dump_yaml(self, mscores, test_dir):
        "test the Scores serialization"
        mscores.dump(filename=os.path.join(test_dir, 'new_scores.yml'))

    def test_scores_get_games(self, mscores):
        """
        test the Scores.get_games method
        :param mscores: the mscores
        """
        assert len(mscores.get_games()) > 0

    def test_game_stat(self):
        "Test the game stat class"
        game_stats = StatsGame('parade')
        new_play = self.__get_play(wintype='min', players='P1=10,p2=1', date='10/01/16')
        game_stats.new_play(new_play)
        assert game_stats.get_highest_score() == new_play
        assert game_stats.get_lowest_score() == new_play
        # add new play
        # lowest
        new_play2 = self.__get_play(wintype='min', players='P1=12,p2=1', date='11/01/16')
        game_stats.new_play(new_play2)
        # highest
        new_play3 = self.__get_play(wintype='min', players='P1=12,p2=0', date='12/01/16')
        game_stats.new_play(new_play3)
        print ('highest score dates expected %s but found %s ' %
               (new_play3.date, game_stats.get_highest_score().date))
        assert game_stats.get_highest_score() == new_play3
        assert game_stats.get_lowest_score() == new_play2
        # test average score !
        assert game_stats.get_average_score() == 36 / 6
        # test best player is p2
        assert game_stats.get_best_player() == 'p2'

    def test_player_stat(self):
        """Test."""
        player_stat = StatsPlayer('test_player')
        assert player_stat
        assert player_stat.__str__() != ''
        assert player_stat.get_worst_ennemy() == ('none', 0)
        assert player_stat.last == 0
        # loss + last
        player_stat.new_play(self.__get_play(players='test_player=0,first=10'))
        # loss + not last
        player_stat.new_play(self.__get_play(players='test_player=5,other=10,last=0'))
        assert player_stat.last == 1

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
        elif players != []:
            for name, score in [player.split('=')
                                for player in players.split(',')]:
                new_play.players.append(Play.create_player(login=name, score=int(score)))
        if winners:
            new_play.winners = winners
        return new_play

    def test_player_stat_winloss_streak(self):
        """
        test the streaks of win or loose
        :return:
        """
        pstat = StatsPlayer('test_player')
        assert pstat.streak_win == 0
        assert pstat.streak_loose == 0
        pstat.new_win()
        assert pstat.streak_win == 1
        assert pstat.streak_win_longest == 1
        assert pstat.streak_loose == 0
        pstat.new_win()
        assert pstat.streak_win == 2
        assert pstat.streak_win_longest == 2
        assert pstat.streak_loose == 0
        pstat.new_loss(['other'])
        assert pstat.streak_win == 0
        assert pstat.streak_loose == 1
        assert pstat.streak_loose_longest == 1
        pstat.new_loss(['other'])
        assert pstat.streak_win == 0
        assert pstat.streak_win_longest == 2
        assert pstat.streak_loose == 2
        assert pstat.streak_loose_longest == 2
        pstat.new_win()
        assert pstat.streak_win == 1
        assert pstat.streak_win_longest == 2
        assert pstat.streak_loose == 0
        assert pstat.streak_loose_longest == 2
        pstat.new_win()
        pstat.new_win()
        pstat.new_win()
        assert pstat.streak_win == 4
        assert pstat.streak_win_longest == 4

    def test_overall_winner_stat(self, mscores, test_dir):
        """Test"""
        overall_stat = OverallWinnerStat()
        overall_stat.new_play(self.__get_play(players='P1=10,p2=1', date='10/01/16'))
        overall_stat.new_play(self.__get_play(players='P1=20,p2=1', date='20/01/16'))
        overall_stat.new_play(self.__get_play(players='P1=30,p2=1', date='30/01/16'))

        assert overall_stat
        assert overall_stat.__str__() != ''
