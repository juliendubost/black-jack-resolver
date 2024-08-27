import pytest
from blackjack.graph import PlayerGraph
from blackjack.constants import MOVE_SURRENDER_ELSE_STAND


@pytest.fixture()
def surrender_graph():
    class SurrenderGraph(PlayerGraph):
        def get_best_move(self, state):
            return MOVE_SURRENDER_ELSE_STAND

    return SurrenderGraph
