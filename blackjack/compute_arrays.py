from blackjack.values import (
    HandState,
    BANK_STARTING_CARDS,
    PLAYER_STARTING_STATES,
    PRE_HIT_CARDS,
    POST_HIT_CARDS,
    HIT_CARDS,
    BANK_STAND_SCORES,
    PLAYER_STAND_STATES,
    STATE_TO_SCORE,
    BANK_STAND_STATES,
)
from decimal import Decimal
from blackjack.transitions import (
    HIT_TRANSITIONS,
    HIT_PROBABILITIES,
)

import numpy as np
from blackjack.ev_montecarlo import ExpectedValue


def score_ev(player_state, bank_state):
    """
    return the player score expected value against final bank state
    """
    # If player is busted, value is 0 even if bank is busted
    if player_state is HandState.BUST:
        return 0
    if bank_state not in BANK_STAND_SCORES:
        raise ValueError(f"bank's final score {bank_state} is forbidden")
    bank_score = STATE_TO_SCORE[bank_state].value
    player_score = STATE_TO_SCORE[player_state].value
    if player_score == bank_score:
        return 1
    if player_score > bank_score:
        return 2 if player_score is not HandState.BLACKJACK else 2.5
    return 0


def hit_transition_matrix():
    """
    compute the hit transition probability matrix for every possible HandState.
    Burned or blackjacd are considered as well
    Example here for hand states starting from 16 (handSate.SIXTEEN) to bust (HandState.BUST)
        16          17      18      19      20      21      BUST
    16  0           1/13    1/13    1/13    1/13    1/13    8/13
    17  0           0       1/13    1/13    1/13    1/13    9/13
    18  0           0       0       1/13    1/13    1/13    10/13
    19  0           0       0       0       1/13    1/13    11/13
    20  0           0       0       0       0       1/13    12/13
    """
    transition_matrix = np.zeros((len(HandState), len(HandState)))
    HIT_CARDS_probability = {
        HandState.ACE: 1 / 13,  # ACE
        HandState.TWO: 1 / 13,  # TWO
        HandState.THREE: 1 / 13,  # THREE
        HandState.FOUR: 1 / 13,  # FOUR
        HandState.FIVE: 1 / 13,  # FIVE
        HandState.SIX: 1 / 13,  # SIX
        HandState.SEVEN: 1 / 13,  # SEVEN
        HandState.EIGHT: 1 / 13,  # EIGHT
        HandState.NINE: 1 / 13,  # NINE
        HandState.FIGURE: 4 / 13,  # FIGURE
    }
    for state_int, row in enumerate(transition_matrix):
        state = HandState(state_int)
        if state in PRE_HIT_CARDS:
            for hit_state in HIT_CARDS:
                probability = HIT_CARDS_probability[hit_state]
                final_state = HIT_TRANSITIONS[state].get(hit_state, HandState.BUST)
                transition_matrix[state.value][final_state.value] += probability
    return transition_matrix
