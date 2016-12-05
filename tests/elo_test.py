#!/usr/bin/env python
# encoding: utf-8

import scores.elo


def test_compute_elo():
    """Test."""
    elo_1, elo_2 = scores.elo.compute_elo(1000, 1000, 1, 2)
    assert (elo_1, elo_2) == (20, -20)
    elo_1, elo_2 = scores.elo.compute_elo(1000, 1000, 2, 1)
    assert (elo_1, elo_2) == (-20, 20)
    elo_1, elo_2 = scores.elo.compute_elo(1000, 1000, 1, 1)
    assert (elo_1, elo_2) == (0, 0)
