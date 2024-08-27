from blackjack.ev import compute_game_ev


def test_surrender_ev(surrender_graph):
    assert round(compute_game_ev(surrender_graph), 2) == 0.5
