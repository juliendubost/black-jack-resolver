import sys

import pytest

from blackjack.graph import BankTransitions, PlayerGraph, score_ev, determine_hand
from blackjack.constants import (
    BANK_STARTING_CARDS,
    STATE_TO_SCORE,
    PLAYER_POSSIBLE_STATES,
    HIT_TRANSITIONS,
    HandState,
)
from blackjack.tests.random import get_bank_score, CardGenerator


class TestBankTransitions:
    def test_final_score_probabilities(self):
        """
        Assert determinist final score probabilities for the bank are correct using a montecarlo validation
        """
        bank_transitions = BankTransitions()
        bank_transitions.build()
        card_generator = CardGenerator()
        final_score_probabilities = bank_transitions.get_final_scores_probabilities()
        sample_size = 100_000
        for start_card in BANK_STARTING_CARDS:
            sys.stdout.write(
                f"Final scores probabilities for start card {start_card} (determined / monte carlo):\n"
            )
            final_scores = {}
            for i in range(sample_size):
                final_score = STATE_TO_SCORE[get_bank_score(start_card, card_generator)]
                if final_score not in final_scores:
                    final_scores[final_score] = 0
                final_scores[final_score] += 1

            for score, count in final_scores.items():
                monte_carlo_probability = round(count / sample_size, 2)
                determinist_probability = round(
                    final_score_probabilities[start_card][score], 2
                )
                sys.stdout.write(
                    f"{score}: {determinist_probability} / {monte_carlo_probability}\n"
                )
                # accept a variation of 0.01001 (= 1 percent point for rounding reasons)
                assert abs(determinist_probability - monte_carlo_probability) <= 0.011


class TestPlayerGraph:
    def assert_stand_ev(self, bank_start_card):
        card_generator = CardGenerator()
        sys.stdout.write(
            f"Stand EVs for bank card {bank_start_card} (determined / monte carlo):\n"
        )
        player_graph = PlayerGraph(bank_start_card)
        player_graph.build()
        for player_state in PLAYER_POSSIBLE_STATES:
            sample_size = 100_000
            stand_ev = round(player_graph.get_stand_ev(player_state), 2)
            montecarlo_absolute_ev = 0
            for i in range(sample_size):
                bank_final_score = STATE_TO_SCORE[
                    get_bank_score(bank_start_card, card_generator)
                ]
                montecarlo_absolute_ev += score_ev(player_state, bank_final_score)
            montecarlo_ev = round(montecarlo_absolute_ev / sample_size, 2)
            sys.stdout.write(f"{player_state}: {stand_ev} / {montecarlo_ev}\n")
            assert abs(stand_ev - montecarlo_ev) <= 0.011

    def test_ace_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for an ace on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.ACE)

    def test_figure_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a figure on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.FIGURE)

    def test_nine_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a nine on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.NINE)

    def test_eight_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for an eight on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.EIGHT)

    def test_seven_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a seven on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.SEVEN)

    def test_six_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a six on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.SIX)

    def test_five_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a five on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.FIVE)

    def test_four_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a four on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.FOUR)

    def test_three_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a three on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.THREE)

    def test_two_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        for a two on bank side
        Use one method for each card to enable pytest-xdist parallelization
        """
        self.assert_stand_ev(HandState.TWO)

    def test_ace_against_sixteen_max_ev(self):
        """
        Assert maximum EV reachable from player state sixteen against an ace on the bank is correct
        """
        card_generator = CardGenerator()
        player_graph = PlayerGraph(HandState.ACE)
        player_graph.build()
        max_ev = player_graph.get_stand_ev(HandState.SIXTEEN)

        absolute_ev = 0
        for i in range(100_000):
            draw_card = card_generator.get()
            after_draw_state = HIT_TRANSITIONS[HandState.SIXTEEN].get(
                draw_card, HandState.BUST
            )
            for (
                bank_score,
                probability,
            ) in player_graph.bank_final_scores_probabilities.items():
                absolute_ev += score_ev(after_draw_state, bank_score) * probability
        draw_ev = absolute_ev / 100_000
        max_ev = max(max_ev, draw_ev)
        sys.stdout.write(
            f"Max EV for bank card {HandState.ACE} and player state {HandState.SIXTEEN} (determined / monte carlo):\n"
        )
        sys.stdout.write(f"{player_graph.max_evs[HandState.SIXTEEN]} / {max_ev}")
        assert abs(player_graph.max_evs[HandState.SIXTEEN] - max_ev) < 0.101


def test_score_ev():
    # Bank have a blackjack
    assert score_ev(HandState.BLACKJACK, HandState.BLACKJACK) == 1
    assert score_ev(HandState.TWENTY_ONE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.TWENTY, HandState.BLACKJACK) == 0
    assert score_ev(HandState.NINE_NINETEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.NINETEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.EIGHT_EIGHTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.EIGHTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.SEVEN_SEVENTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.SEVENTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.SIX_SIXTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.SIXTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FIVE_FIFTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FIFTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FOUR_FOURTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FOURTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.THREE_THIRTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.THIRTEEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.TWO_TWELVE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.TWELVE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.ELEVEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.TEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FIGURE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.NINE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.EIGHT, HandState.BLACKJACK) == 0
    assert score_ev(HandState.SEVEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.SIX, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FIVE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.FOUR, HandState.BLACKJACK) == 0
    assert score_ev(HandState.THREE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.TWO, HandState.BLACKJACK) == 0
    assert score_ev(HandState.ACE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_TWO, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_THREE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_FOUR, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_FIVE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_SIX, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_SEVEN, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_EIGHT, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_NINE, HandState.BLACKJACK) == 0
    assert score_ev(HandState.POCKET_FIGURE, HandState.BLACKJACK) == 0

    # Bank have a 21
    assert score_ev(HandState.BLACKJACK, HandState.TWENTY_ONE) == 2.5
    assert score_ev(HandState.TWENTY_ONE, HandState.TWENTY_ONE) == 1
    assert score_ev(HandState.TWENTY, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.NINE_NINETEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.NINETEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.EIGHT_EIGHTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.EIGHTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.SEVEN_SEVENTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.SEVENTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.SIX_SIXTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.SIXTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FIVE_FIFTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FIFTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FOUR_FOURTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FOURTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.THREE_THIRTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.THIRTEEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.TWO_TWELVE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.TWELVE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.ELEVEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.TEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FIGURE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.NINE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.EIGHT, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.SEVEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.SIX, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FIVE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.FOUR, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.THREE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.TWO, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.ACE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_TWO, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_THREE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_FOUR, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_FIVE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_SIX, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_SEVEN, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_EIGHT, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_NINE, HandState.TWENTY_ONE) == 0
    assert score_ev(HandState.POCKET_FIGURE, HandState.TWENTY_ONE) == 0

    # Bank have a 20
    assert score_ev(HandState.BLACKJACK, HandState.TWENTY) == 2.5
    assert score_ev(HandState.TWENTY_ONE, HandState.TWENTY) == 2
    assert score_ev(HandState.TWENTY, HandState.TWENTY) == 1
    assert score_ev(HandState.NINE_NINETEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.NINETEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.EIGHT_EIGHTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.EIGHTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.SEVEN_SEVENTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.SEVENTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.SIX_SIXTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.SIXTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.FIVE_FIFTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.FIFTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.FOUR_FOURTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.FOURTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.THREE_THIRTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.THIRTEEN, HandState.TWENTY) == 0
    assert score_ev(HandState.TWO_TWELVE, HandState.TWENTY) == 0
    assert score_ev(HandState.TWELVE, HandState.TWENTY) == 0
    assert score_ev(HandState.ELEVEN, HandState.TWENTY) == 0
    assert score_ev(HandState.TEN, HandState.TWENTY) == 0
    assert score_ev(HandState.FIGURE, HandState.TWENTY) == 0
    assert score_ev(HandState.NINE, HandState.TWENTY) == 0
    assert score_ev(HandState.EIGHT, HandState.TWENTY) == 0
    assert score_ev(HandState.SEVEN, HandState.TWENTY) == 0
    assert score_ev(HandState.SIX, HandState.TWENTY) == 0
    assert score_ev(HandState.FIVE, HandState.TWENTY) == 0
    assert score_ev(HandState.FOUR, HandState.TWENTY) == 0
    assert score_ev(HandState.THREE, HandState.TWENTY) == 0
    assert score_ev(HandState.TWO, HandState.TWENTY) == 0
    assert score_ev(HandState.ACE, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_TWO, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_THREE, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_FOUR, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_FIVE, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_SIX, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_SEVEN, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_EIGHT, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_NINE, HandState.TWENTY) == 0
    assert score_ev(HandState.POCKET_FIGURE, HandState.TWENTY) == 1

    # Bank have a 19
    assert score_ev(HandState.BLACKJACK, HandState.NINETEEN) == 2.5
    assert score_ev(HandState.TWENTY_ONE, HandState.NINETEEN) == 2
    assert score_ev(HandState.TWENTY, HandState.NINETEEN) == 2
    assert score_ev(HandState.NINE_NINETEEN, HandState.NINETEEN) == 1
    assert score_ev(HandState.NINETEEN, HandState.NINETEEN) == 1
    assert score_ev(HandState.EIGHT_EIGHTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.EIGHTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.SEVEN_SEVENTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.SEVENTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.SIX_SIXTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.SIXTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.FIVE_FIFTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.FIFTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.FOUR_FOURTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.FOURTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.THREE_THIRTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.THIRTEEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.TWO_TWELVE, HandState.NINETEEN) == 0
    assert score_ev(HandState.TWELVE, HandState.NINETEEN) == 0
    assert score_ev(HandState.ELEVEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.TEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.FIGURE, HandState.NINETEEN) == 0
    assert score_ev(HandState.NINE, HandState.NINETEEN) == 0
    assert score_ev(HandState.EIGHT, HandState.NINETEEN) == 0
    assert score_ev(HandState.SEVEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.SIX, HandState.NINETEEN) == 0
    assert score_ev(HandState.FIVE, HandState.NINETEEN) == 0
    assert score_ev(HandState.FOUR, HandState.NINETEEN) == 0
    assert score_ev(HandState.THREE, HandState.NINETEEN) == 0
    assert score_ev(HandState.TWO, HandState.NINETEEN) == 0
    assert score_ev(HandState.ACE, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_TWO, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_THREE, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_FOUR, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_FIVE, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_SIX, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_SEVEN, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_EIGHT, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_NINE, HandState.NINETEEN) == 0
    assert score_ev(HandState.POCKET_FIGURE, HandState.NINETEEN) == 2

    # Bank have a 18
    assert score_ev(HandState.BLACKJACK, HandState.EIGHTEEN) == 2.5
    assert score_ev(HandState.TWENTY_ONE, HandState.EIGHTEEN) == 2
    assert score_ev(HandState.TWENTY, HandState.EIGHTEEN) == 2
    assert score_ev(HandState.NINE_NINETEEN, HandState.EIGHTEEN) == 2
    assert score_ev(HandState.NINETEEN, HandState.EIGHTEEN) == 2
    assert score_ev(HandState.EIGHT_EIGHTEEN, HandState.EIGHTEEN) == 1
    assert score_ev(HandState.EIGHTEEN, HandState.EIGHTEEN) == 1
    assert score_ev(HandState.SEVEN_SEVENTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.SEVENTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.SIX_SIXTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.SIXTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FIVE_FIFTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FIFTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FOUR_FOURTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FOURTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.THREE_THIRTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.THIRTEEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.TWO_TWELVE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.TWELVE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.ELEVEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.TEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FIGURE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.NINE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.EIGHT, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.SEVEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.SIX, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FIVE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.FOUR, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.THREE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.TWO, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.ACE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_TWO, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_THREE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_FOUR, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_FIVE, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_SIX, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_SEVEN, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_EIGHT, HandState.EIGHTEEN) == 0
    assert score_ev(HandState.POCKET_NINE, HandState.EIGHTEEN) == 1
    assert score_ev(HandState.POCKET_FIGURE, HandState.EIGHTEEN) == 2

    # Bank have a 17
    assert score_ev(HandState.BLACKJACK, HandState.SEVENTEEN) == 2.5
    assert score_ev(HandState.TWENTY_ONE, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.TWENTY, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.NINE_NINETEEN, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.NINETEEN, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.EIGHT_EIGHTEEN, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.EIGHTEEN, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.SEVEN_SEVENTEEN, HandState.SEVENTEEN) == 1
    assert score_ev(HandState.SEVENTEEN, HandState.SEVENTEEN) == 1
    assert score_ev(HandState.SIX_SIXTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.SIXTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FIVE_FIFTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FIFTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FOUR_FOURTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FOURTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.THREE_THIRTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.THIRTEEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.TWO_TWELVE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.TWELVE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.ELEVEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.TEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FIGURE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.NINE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.EIGHT, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.SEVEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.SIX, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FIVE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.FOUR, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.THREE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.TWO, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.ACE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_TWO, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_THREE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_FOUR, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_FIVE, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_SIX, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_SEVEN, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_EIGHT, HandState.SEVENTEEN) == 0
    assert score_ev(HandState.POCKET_NINE, HandState.SEVENTEEN) == 2
    assert score_ev(HandState.POCKET_FIGURE, HandState.SEVENTEEN) == 2


def test_determine_hand():
    # pocket hands
    assert determine_hand(HandState.ACE, HandState.ACE) == HandState.POCKET_ACE
    assert determine_hand(HandState.TWO, HandState.TWO) == HandState.POCKET_TWO
    assert determine_hand(HandState.THREE, HandState.THREE) == HandState.POCKET_THREE
    assert determine_hand(HandState.FOUR, HandState.FOUR) == HandState.POCKET_FOUR
    assert determine_hand(HandState.FIVE, HandState.FIVE) == HandState.POCKET_FIVE
    assert determine_hand(HandState.SIX, HandState.SIX) == HandState.POCKET_SIX
    assert determine_hand(HandState.SEVEN, HandState.SEVEN) == HandState.POCKET_SEVEN
    assert determine_hand(HandState.EIGHT, HandState.EIGHT) == HandState.POCKET_EIGHT
    assert (
        determine_hand(
            HandState.NINE,
            HandState.NINE,
        )
        == HandState.POCKET_NINE
    )
    assert determine_hand(HandState.FIGURE, HandState.FIGURE) == HandState.POCKET_FIGURE
    with pytest.raises(KeyError):  # TEN is not a start card and should be allowed
        determine_hand(HandState.TEN, HandState.TEN)

    # soft states
    assert determine_hand(HandState.ACE, HandState.TWO) == HandState.THREE_THIRTEEN
    assert determine_hand(HandState.TWO, HandState.ACE) == HandState.THREE_THIRTEEN
    assert determine_hand(HandState.ACE, HandState.THREE) == HandState.FOUR_FOURTEEN
    assert determine_hand(HandState.THREE, HandState.ACE) == HandState.FOUR_FOURTEEN
    assert determine_hand(HandState.ACE, HandState.FOUR) == HandState.FIVE_FIFTEEN
    assert determine_hand(HandState.FOUR, HandState.ACE) == HandState.FIVE_FIFTEEN
    assert determine_hand(HandState.ACE, HandState.FIVE) == HandState.SIX_SIXTEEN
    assert determine_hand(HandState.FIVE, HandState.ACE) == HandState.SIX_SIXTEEN
    assert determine_hand(HandState.ACE, HandState.SIX) == HandState.SEVEN_SEVENTEEN
    assert determine_hand(HandState.SIX, HandState.ACE) == HandState.SEVEN_SEVENTEEN
    assert determine_hand(HandState.ACE, HandState.SEVEN) == HandState.EIGHT_EIGHTEEN
    assert determine_hand(HandState.SEVEN, HandState.ACE) == HandState.EIGHT_EIGHTEEN
    assert determine_hand(HandState.ACE, HandState.EIGHT) == HandState.NINE_NINETEEN
    assert determine_hand(HandState.EIGHT, HandState.ACE) == HandState.NINE_NINETEEN
    assert determine_hand(HandState.ACE, HandState.NINE) == HandState.TEN_TWENTY
    assert determine_hand(HandState.NINE, HandState.ACE) == HandState.TEN_TWENTY
    assert determine_hand(HandState.ACE, HandState.FIGURE) == HandState.BLACKJACK
    assert determine_hand(HandState.FIGURE, HandState.ACE) == HandState.BLACKJACK
    with pytest.raises(KeyError):  # TEN is not a start card and should be allowed
        determine_hand(HandState.ACE, HandState.TEN)
    with pytest.raises(KeyError):  # TEN is not a start card and should be allowed
        determine_hand(HandState.TEN, HandState.ACE)

    # hard states
    assert determine_hand(HandState.TWO, HandState.THREE) == HandState.FIVE
    assert determine_hand(HandState.THREE, HandState.TWO) == HandState.FIVE
    assert determine_hand(HandState.TWO, HandState.FOUR) == HandState.SIX
    assert determine_hand(HandState.FOUR, HandState.TWO) == HandState.SIX
    assert determine_hand(HandState.TWO, HandState.FIVE) == HandState.SEVEN
    assert determine_hand(HandState.FIVE, HandState.TWO) == HandState.SEVEN
    assert determine_hand(HandState.TWO, HandState.SIX) == HandState.EIGHT
    assert determine_hand(HandState.SIX, HandState.TWO) == HandState.EIGHT
    assert determine_hand(HandState.TWO, HandState.SEVEN) == HandState.NINE
    assert determine_hand(HandState.SEVEN, HandState.TWO) == HandState.NINE
    assert determine_hand(HandState.TWO, HandState.EIGHT) == HandState.TEN
    assert determine_hand(HandState.EIGHT, HandState.TWO) == HandState.TEN
    assert determine_hand(HandState.TWO, HandState.NINE) == HandState.ELEVEN
    assert determine_hand(HandState.NINE, HandState.TWO) == HandState.ELEVEN
    assert determine_hand(HandState.TWO, HandState.FIGURE) == HandState.TWELVE
    assert determine_hand(HandState.FIGURE, HandState.TWO) == HandState.TWELVE

    assert determine_hand(HandState.THREE, HandState.FOUR) == HandState.SEVEN
    assert determine_hand(HandState.FOUR, HandState.THREE) == HandState.SEVEN
    assert determine_hand(HandState.THREE, HandState.FIVE) == HandState.EIGHT
    assert determine_hand(HandState.FIVE, HandState.THREE) == HandState.EIGHT
    assert determine_hand(HandState.THREE, HandState.SIX) == HandState.NINE
    assert determine_hand(HandState.SIX, HandState.THREE) == HandState.NINE
    assert determine_hand(HandState.THREE, HandState.SEVEN) == HandState.TEN
    assert determine_hand(HandState.SEVEN, HandState.THREE) == HandState.TEN
    assert determine_hand(HandState.THREE, HandState.EIGHT) == HandState.ELEVEN
    assert determine_hand(HandState.EIGHT, HandState.THREE) == HandState.ELEVEN
    assert determine_hand(HandState.THREE, HandState.NINE) == HandState.TWELVE
    assert determine_hand(HandState.NINE, HandState.THREE) == HandState.TWELVE
    assert determine_hand(HandState.THREE, HandState.FIGURE) == HandState.THIRTEEN
    assert determine_hand(HandState.FIGURE, HandState.THREE) == HandState.THIRTEEN

    assert determine_hand(HandState.FOUR, HandState.FIVE) == HandState.NINE
    assert determine_hand(HandState.FIVE, HandState.FOUR) == HandState.NINE
    assert determine_hand(HandState.FOUR, HandState.SIX) == HandState.TEN
    assert determine_hand(HandState.SIX, HandState.FOUR) == HandState.TEN
    assert determine_hand(HandState.FOUR, HandState.SEVEN) == HandState.ELEVEN
    assert determine_hand(HandState.SEVEN, HandState.FOUR) == HandState.ELEVEN
    assert determine_hand(HandState.FOUR, HandState.EIGHT) == HandState.TWELVE
    assert determine_hand(HandState.EIGHT, HandState.FOUR) == HandState.TWELVE
    assert determine_hand(HandState.FOUR, HandState.NINE) == HandState.THIRTEEN
    assert determine_hand(HandState.NINE, HandState.FOUR) == HandState.THIRTEEN
    assert determine_hand(HandState.FOUR, HandState.FIGURE) == HandState.FOURTEEN
    assert determine_hand(HandState.FIGURE, HandState.FOUR) == HandState.FOURTEEN

    assert determine_hand(HandState.FIVE, HandState.SIX) == HandState.ELEVEN
    assert determine_hand(HandState.SIX, HandState.FIVE) == HandState.ELEVEN
    assert determine_hand(HandState.FIVE, HandState.SEVEN) == HandState.TWELVE
    assert determine_hand(HandState.SEVEN, HandState.FIVE) == HandState.TWELVE
    assert determine_hand(HandState.FIVE, HandState.EIGHT) == HandState.THIRTEEN
    assert determine_hand(HandState.EIGHT, HandState.FIVE) == HandState.THIRTEEN
    assert determine_hand(HandState.FIVE, HandState.NINE) == HandState.FOURTEEN
    assert determine_hand(HandState.NINE, HandState.FIVE) == HandState.FOURTEEN
    assert determine_hand(HandState.FIVE, HandState.FIGURE) == HandState.FIFTEEN
    assert determine_hand(HandState.FIGURE, HandState.FIVE) == HandState.FIFTEEN

    assert determine_hand(HandState.SIX, HandState.SEVEN) == HandState.THIRTEEN
    assert determine_hand(HandState.SEVEN, HandState.SIX) == HandState.THIRTEEN
    assert determine_hand(HandState.SIX, HandState.EIGHT) == HandState.FOURTEEN
    assert determine_hand(HandState.EIGHT, HandState.SIX) == HandState.FOURTEEN
    assert determine_hand(HandState.SIX, HandState.NINE) == HandState.FIFTEEN
    assert determine_hand(HandState.NINE, HandState.SIX) == HandState.FIFTEEN
    assert determine_hand(HandState.SIX, HandState.FIGURE) == HandState.SIXTEEN
    assert determine_hand(HandState.FIGURE, HandState.SIX) == HandState.SIXTEEN

    assert determine_hand(HandState.SEVEN, HandState.EIGHT) == HandState.FIFTEEN
    assert determine_hand(HandState.EIGHT, HandState.SEVEN) == HandState.FIFTEEN
    assert determine_hand(HandState.SEVEN, HandState.NINE) == HandState.SIXTEEN
    assert determine_hand(HandState.NINE, HandState.SEVEN) == HandState.SIXTEEN
    assert determine_hand(HandState.SEVEN, HandState.FIGURE) == HandState.SEVENTEEN
    assert determine_hand(HandState.FIGURE, HandState.SEVEN) == HandState.SEVENTEEN

    assert determine_hand(HandState.EIGHT, HandState.NINE) == HandState.SEVENTEEN
    assert determine_hand(HandState.NINE, HandState.EIGHT) == HandState.SEVENTEEN
    assert determine_hand(HandState.EIGHT, HandState.FIGURE) == HandState.EIGHTEEN
    assert determine_hand(HandState.FIGURE, HandState.EIGHT) == HandState.EIGHTEEN

    assert determine_hand(HandState.NINE, HandState.FIGURE) == HandState.NINETEEN
    assert determine_hand(HandState.FIGURE, HandState.NINE) == HandState.NINETEEN
