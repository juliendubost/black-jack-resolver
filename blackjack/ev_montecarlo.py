import math

import numpy as np
from enum import Enum
from blackjack.values import HandState
from blackjack.transitions import HIT_TRANSITIONS


class Actions(Enum):
    HIT = 0
    STAND = 1
    DOUBLE = 3
    RESIGN = 4
    SPARE = 5


class Drawer:
    def __init__(self):
        self.values = np.array(
            [
                HandState.ACE,
                HandState.TWO,
                HandState.THREE,
                HandState.FOUR,
                HandState.FIVE,
                HandState.SIX,
                HandState.SEVEN,
                HandState.EIGHT,
                HandState.NINE,
                HandState.FIGURE,
            ]
        )
        # probability distribution for card values
        self.distributions = np.array(
            [
                1 / 13,
                1 / 13,
                1 / 13,
                1 / 13,
                1 / 13,
                1 / 13,
                1 / 13,
                1 / 13,
                1 / 13,
                4 / 13,
            ]
        )

    def draw(self):
        return np.random.choice(self.values, p=self.distributions)

    def get_bank_final_score(self, initial_score):
        """
        Bank stand at 7-17 and more, hit at 6-16 or less
        """
        final_score = initial_score
        while final_score not in [
            HandState.BUST,
            HandState.SEVEN_SEVENTEEN,
            HandState.SEVENTEEN,
            HandState.EIGHTEEN,
            HandState.EIGHT_EIGHTEEN,
            HandState.NINETEEN,
            HandState.NINE_NINETEEN,
            HandState.TWENTY,
            HandState.TEN_TWENTY,
            HandState.TWENTY_ONE,
            HandState.BLACKJACK,
        ]:
            card_value = self.draw()
            final_score = HIT_TRANSITIONS[final_score].get(card_value, HandState.BUST)
        return final_score


class ExpectedValue:
    """
    Compute the expected value and the variation coefficient for a given player standing score with a given bank score
    """

    def __init__(
            self,
            player_score,
            bank_score,
            batch_size=1000,
            batchs=100,
            cut_treshold_percent=1,
    ):
        """"""
        self.player_score = player_score
        self.bank_score = bank_score
        self.batch_size = batch_size
        self.batchs = batchs
        self.cut_treshold_percent = cut_treshold_percent
        self.mean_expected_value = None
        self.standard_deviation = None
        self.drawer = Drawer()

    def compute(self):
        batch = 1
        batch_deviations_squared = []
        while batch < (self.batchs + 1):
            batch_draw = 0
            batch_mean_expected_value = 0
            while batch_draw < self.batch_size:
                batch_draw += 1
                _, bank_final_score = self.drawer.get_bank_final_score(
                    self.bank_score
                ).value
                _, player_score = self.player_score.value
                if bank_final_score is None or (bank_final_score < player_score):
                    # bank hand is burned, player wins
                    if self.player_score == HandState.BLACKJACK:
                        sample_expected_value = 2.5
                    else:
                        sample_expected_value = 2
                elif bank_final_score == player_score:
                    sample_expected_value = 1  # tie
                else:
                    sample_expected_value = (
                        0  # bank final score is better, player loose
                    )
                batch_mean_expected_value += sample_expected_value / self.batch_size
            if batch == 1:
                self.mean_expected_value = batch_mean_expected_value
            else:
                self.mean_expected_value = (
                                                   batch_mean_expected_value + self.mean_expected_value * (batch - 1)
                                           ) / batch
            batch_deviations_squared.append(
                (batch_mean_expected_value - self.mean_expected_value) ** 2
            )
            self.standard_deviation = math.sqrt(
                sum(batch_deviations_squared) / len(batch_deviations_squared)
            )
            batch += 1
        print("-------------")
        print(f"mean_expected_value: {self.mean_expected_value}")
        print(f"standard_deviation: {self.standard_deviation}")
        print("-------------")
