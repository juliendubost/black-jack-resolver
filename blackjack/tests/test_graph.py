import sys

from blackjack.graph import BankTransitions, PlayerGraph, score_ev
from blackjack.constants import (
    BANK_STARTING_CARDS,
    STATE_TO_SCORE,
    PLAYER_POSSIBLE_STATES,
    HandState,
)
from blackjack.tests.simulator import get_bank_score, CardGenerator


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
                # accept a variation of 0.011 (= 1.1 percent point)
                assert abs(determinist_probability - monte_carlo_probability) <= 0.011


class TestPlayerGraph:
    def test_stand_ev(self):
        """
        Assert determinist stand expected values are correct using a montecarlo validation
        """
        card_generator = CardGenerator()
        for bank_start_card in BANK_STARTING_CARDS:
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
