from blackjack.graph import PlayerGraph
from blackjack import constants


def compute_game_ev(graph_class):
    """
    Compute the whole game expected value
    graph_class: one of PlayerGraph or BasicStrategyGraph

    return: positive float where:
        0.0 mean game have no EV, like if you loose every time you bet
        1.0 mean game is even, your return on investment is 0%
        2.0 mean game is EV+, you return on investment is 100%, you get a total of 2 every time you bet 1
        1.5 mean game is EV+, you return on investment is 50%, you get a total of 1.5 every time you bet 1
    """
    # compute expected value against each bank card
    player_abs_val = 0  # total absolute value for the player
    for bank_card in constants.BANK_STARTING_CARDS:
        bank_card_probability = (
            1 / 13 if bank_card != constants.HandState.FIGURE else 4 / 13
        )
        player_graph = graph_class(bank_card)
        player_graph.build()
        for player_hand, probability in constants.START_HAND_PROBABILITIES.items():
            best_move = player_graph.get_best_move(player_hand)
            if best_move in [
                constants.MOVE_STAND,
                constants.MOVE_HIT,
            ]:
                player_abs_val += (
                    probability
                    * bank_card_probability
                    * (player_graph.max_evs[player_hand] - 1)
                )
            elif best_move in [
                constants.MOVE_DOUBLE,
                constants.MOVE_DOUBLE_ELSE_HIT,
                constants.MOVE_DOUBLE_ELSE_STAND,
            ]:
                player_abs_val += (
                    2
                    * bank_card_probability
                    * probability
                    * (player_graph.hit_evs[player_hand] - 1)
                )
            elif best_move in [
                constants.MOVE_SURRENDER_ELSE_STAND,
                constants.MOVE_SURRENDER_ELSE_HIT,
                constants.MOVE_SURRENDER_ELSE_SPLIT,
            ]:
                player_abs_val += -bank_card_probability * probability * 0.5
            elif best_move == constants.MOVE_SPLIT:
                post_split_state = constants.POST_SPLIT_STATE[player_hand]
                player_abs_val += (
                    2
                    * bank_card_probability
                    * probability
                    * (player_graph.max_evs[post_split_state] - 1)
                )
            else:
                raise ValueError(f"Unknown move {best_move}")

    return 1 + player_abs_val
