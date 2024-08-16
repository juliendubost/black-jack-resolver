from blackjack.constants import HandState
import random


class CardGenerator:

    def __init__(self):
        self.sysrandom = random.SystemRandom()
        self.cards = [HandState.ACE,
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
        Get a random card
        0: an Ace

        """
        return self.sysrandom.choice(self.cards)






