from blackjack.graph import PlayerGraph
from blackjack import constants


def compute_game_ev():
    """
    Compute the whole game expected value
    """
    # compute ev against each bank card
    player_abs_ev = 0  # total absolute EV for the player
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
                constants.MOVE_SPLIT,
            ]:
                # TODO: consider split EV
                player_abs_ev += (
                    probability
                    * bank_card_probability
                    * (player_graph.max_evs[player_hand])
                )
            elif best_move in [
                constants.MOVE_DOUBLE,
                constants.MOVE_DOUBLE_ELSE_HIT,
                constants.MOVE_DOUBLE_ELSE_STAND,
            ]:
                player_abs_ev += (
                    2
                    * bank_card_probability
                    * probability
                    * (player_graph.hit_evs[player_hand])
                )
            elif best_move in [
                constants.MOVE_SURRENDER_ELSE_STAND,
                constants.MOVE_SURRENDER_ELSE_HIT,
                constants.MOVE_SURRENDER_ELSE_SPLIT,
            ]:
                player_abs_ev += bank_card_probability * 0.5

    return player_abs_ev
