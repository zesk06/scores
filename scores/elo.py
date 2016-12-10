#!/usr/bin/env python
# encoding: utf-8

"""
    A module to compute ELOs
"""

K = 100

F = 1500

S_VICT = 1
S_DRAW = 0.5
S_LOSS = 0


def compute_elo(elo_1, elo_2, rank_1, rank_2, k_factor=K):
    """Return the ELO change between 2 players ranked game
    :param elo_1: The first player ELO before the game
    :param elo_2: The second player ELO before the game
    :param rank_1: The first player game's rank (1 means victory)
    :param rank_2: The second player game's rank (1 means victory)
    """
    expected_1 = float(1) / (1 + pow(10, (float(elo_2)-elo_1)/F))
    expected_2 = float(1) / (1 + pow(10, (float(elo_1)-elo_2)/F))

    if rank_1 < rank_2:
        score_1 = S_VICT
        score_2 = S_LOSS
    elif rank_2 < rank_1:
        score_1 = S_LOSS
        score_2 = S_VICT
    else:
        score_1 = S_DRAW
        score_2 = S_DRAW

    elo_1_diff = k_factor * (score_1 - expected_1)
    elo_2_diff = k_factor * (score_2 - expected_2)

    return (int(elo_1_diff), int(elo_2_diff))


def compute_elos(player_elos, players_rank, k_factor=K):
    """Compute and return the ELOs variation
    :param player_elos: the player initial ELOs
    :type player_elos: list(int)
    :param players_rank: The players play rank
    :type player_rank: list(int)
    :rtype: list(int)
    """
    if len(player_elos) != len(players_rank):
        raise RuntimeError('list length must match %s != %s' % (player_elos, players_rank))
    player_nb = len(player_elos)
    elo_diff = []
    for _ in range(0, player_nb):
        elo_diff.append(0)
    for player_1 in range(0, player_nb):
        # compute elo variation against each other player
        for player_2 in range(player_1 + 1, player_nb):
            elo_1 = player_elos[player_1]
            rank_1 = players_rank[player_1]
            elo_2 = player_elos[player_2]
            rank_2 = players_rank[player_2]
            elo_1_diff, elo_2_diff = compute_elo(elo_1, elo_2, rank_1, rank_2, k_factor)
            elo_diff[player_1] += elo_1_diff
            elo_diff[player_2] += elo_2_diff
    return elo_diff
