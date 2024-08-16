from blackjack.tests.generator import CardGenerator
from blackjack.constants import HandState
import sys


def test_generator():
    """
    Assert the generator draw is balanced
    Display stats after each batchs
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


