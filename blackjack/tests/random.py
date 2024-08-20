import random
from blackjack.constants import (
    HandState,
    BANK_STAND_SCORES,
    HIT_TRANSITIONS,
    STATE_TO_SCORE,
)


class CardGenerator:
    def __init__(self):
        self.sysrandom = random.SystemRandom()
        self.cards = [
            HandState.ACE,
            HandState.TWO,
            HandState.THREE,
            HandState.FOUR,
            HandState.FIVE,
            HandState.SIX,
            HandState.SEVEN,
            HandState.EIGHT,
            HandState.NINE,
            HandState.FIGURE,  # represent a 10
            HandState.FIGURE,  # represent a jack
            HandState.FIGURE,  # represent a queen
            HandState.FIGURE,  # represent a king
        ]

    def get(self):
        """
        Get a random card from self.cards
        """
        return self.sysrandom.choice(self.cards)


def get_bank_score(initial_state, card_generator):
    """
    Given an initial state, return a final bank score using random cards
    Hit cards until bank state is final
    """
    state = initial_state
    while STATE_TO_SCORE[state] not in BANK_STAND_SCORES:
        state = HIT_TRANSITIONS[state].get(card_generator.get(), HandState.BUST)

    return state
