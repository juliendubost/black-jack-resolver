import sys
import copy

from blackjack.tests.simulator import CardGenerator, get_bank_score
from blackjack.constants import HandState, BANK_STARTING_CARDS, BANK_STAND_STATES


def test_card_generator():
    """
    Assert the card draw generator is balanced
    Display a line of statistics after each batch
    """
    card_generator = CardGenerator()

    hits = {
        HandState.ACE: 0,
        HandState.TWO: 0,
        HandState.THREE: 0,
        HandState.FOUR: 0,
        HandState.FIVE: 0,
        HandState.SIX: 0,
        HandState.SEVEN: 0,
        HandState.EIGHT: 0,
        HandState.NINE: 0,
        HandState.FIGURE: 0,
    }
    total = 0

    sys.stdout.write("\n")
    sys.stdout.write("A\t2\t3\t4\t5\t6\t7\t8\t9\tF\n")
    for batch in range(0, 1000):
        for sample in range(0, 1000):
            hits[card_generator.get()] += 1
            total += 1
        for card, value in hits.items():
            sys.stdout.write(f"{round(value/total, 2)}%\t")
        sys.stdout.write("\r")
    sys.stdout.write("\n")

    assert round(hits[HandState.ACE] / total, 2) == 0.08
    assert round(hits[HandState.TWO] / total, 2) == 0.08
    assert round(hits[HandState.THREE] / total, 2) == 0.08
    assert round(hits[HandState.FOUR] / total, 2) == 0.08
    assert round(hits[HandState.FIVE] / total, 2) == 0.08
    assert round(hits[HandState.SIX] / total, 2) == 0.08
    assert round(hits[HandState.SEVEN] / total, 2) == 0.08
    assert round(hits[HandState.EIGHT] / total, 2) == 0.08
    assert round(hits[HandState.NINE] / total, 2) == 0.08
    assert round(hits[HandState.FIGURE] / total, 2) == 0.31


def test_bank_score():
    """
    Assert bank's final score is always one of BANK_STAND_STATES
    """
    card_generator = CardGenerator()
    for start_card in BANK_STARTING_CARDS:
        final_states = set()
        possible_states = copy.deepcopy(BANK_STAND_STATES)

        # Remove blackjack if start card is not a 10-valued card or an ace
        if start_card not in [HandState.ACE, HandState.FIGURE]:
            possible_states.remove(HandState.BLACKJACK)

        # Remove 8-18 is start card is a 6, 9 or 10-valued card since this state is not possible
        if start_card in [HandState.SIX, HandState.NINE, HandState.FIGURE]:
            possible_states.remove(HandState.EIGHT_EIGHTEEN)

        # Remove 9-19 is start card is a 7 or a ten-valued card since this state is not possible
        if start_card == [HandState.SEVEN, HandState.FIGURE]:
            possible_states.remove(HandState.NINE_NINETEEN)

        # Remove 10-20 is start card is a 8 or a ten-valued card since this state is not possible
        if start_card in [HandState.EIGHT, HandState.FIGURE]:
            possible_states.remove(HandState.TEN_TWENTY)

        for i in range(50000):
            final_states.add(get_bank_score(start_card, card_generator))
        for final_state in possible_states:
            assert final_state in possible_states
        sys.stdout.write(f"All bank final scores found for start card {start_card}\n")
