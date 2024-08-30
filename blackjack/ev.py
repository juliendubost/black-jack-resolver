from blackjack import constants
from blackjack import settings


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

    bank_starting_card_probabilities = {}
    if settings.DEALER_PEEKED:
        # Add an abstract blackjack hand to compensate the miss of blackjack possibility for ace and figure EV table
        # if dealer peeked option is ON
        black_jack_probability_on_ace_or_figure = (
            1 / 13 * 4 / 13
        )  # probability to have an ACE then a ten-valued card or vice versa
        bank_starting_card_probabilities[constants.HandState.ACE] = (
            1 / 13 - black_jack_probability_on_ace_or_figure
        )
        bank_starting_card_probabilities[constants.HandState.TWO] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.THREE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.FOUR] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.FIVE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.SIX] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.SEVEN] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.EIGHT] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.NINE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.FIGURE] = (
            4 / 13 - black_jack_probability_on_ace_or_figure
        )
        bank_starting_card_probabilities[constants.HandState.BLACKJACK] = (
            2 * black_jack_probability_on_ace_or_figure
        )
    else:
        bank_starting_card_probabilities[constants.HandState.ACE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.TWO] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.THREE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.FOUR] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.FIVE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.SIX] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.SEVEN] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.EIGHT] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.NINE] = 1 / 13
        bank_starting_card_probabilities[constants.HandState.FIGURE] = 4 / 13

    for bank_card, bank_card_probability in bank_starting_card_probabilities.items():
        # special case for special blacjack bank card
        if bank_card == constants.HandState.BLACKJACK:
            for player_hand, probability in constants.START_HAND_PROBABILITIES.items():
                if player_hand != constants.HandState.BLACKJACK:
                    player_abs_val += -bank_card_probability * probability
            continue

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
