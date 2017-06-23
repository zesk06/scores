#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=C0111

import scores.stats.stats_elo as stats_elo


def test_new_play():
    stats = stats_elo.StatsElo()
    assert stats.elos_per_player == {}
    assert stats.elos_per_player == {}
