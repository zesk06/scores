#!/usr/bin/env python
# encoding: utf-8

import scores.elo


def test_compute_elo():
    """Test."""
    elo_1, elo_2 = scores.elo.compute_elo(1000, 1000, 1, 2)
    assert (elo_1, elo_2) == (50, -50)
    elo_1, elo_2 = scores.elo.compute_elo(1000, 1000, 2, 1)
    assert (elo_1, elo_2) == (-50, 50)
    elo_1, elo_2 = scores.elo.compute_elo(1000, 1000, 1, 1)
    assert (elo_1, elo_2) == (0, 0)
    elo_1, elo_2 = scores.elo.compute_elo(2000, 1000, 1, 2)
    assert (elo_1, elo_2) == (17, -17)
    elo_1, elo_2 = scores.elo.compute_elo(1000, 2000, 1, 2)
    assert (elo_1, elo_2) == (82, -82)
    elo_1, elo_2 = scores.elo.compute_elo(3000, 1000, 1, 2)
    assert (elo_1, elo_2) == (4, -4)
    elo_1, elo_2 = scores.elo.compute_elo(3000, 1000, 2, 1)
    assert (elo_1, elo_2) == (-95, 95)
