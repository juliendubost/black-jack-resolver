from blackjack.graph import PlayerGraph
from blackjack import constants


def compute_game_ev():
    """
    Compute the whole game expected value
    """
    # compute expected value against each bank card
    player_abs_val = 0  # total absolute value for the player
    for bank_card in constants.BANK_STARTING_CARDS:
        bank_card_probability = (
            1 / 13 if bank_card != constants.HandState.FIGURE else 4 / 13
        )
        player_graph = PlayerGraph(bank_card)
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

    return player_abs_val
