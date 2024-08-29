from blackjack.ev import compute_game_ev


def test_surrender_ev(surrender_graph):
    """
    Use a full surerender strategy to check if computed game EV is equal 0.5 which is theoretically expected
    """
    assert round(compute_game_ev(surrender_graph), 2) == 0.5
