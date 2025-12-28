from blackjack.constants import START_HAND_PROBABILITIES
from blackjack.tests.random import CardGenerator
from blackjack.graph import determine_hand


def test_start_hand_weights():
    simulated_start_hands = {}
    sample_size = 5_000_000

    card_generator = CardGenerator()
    for i in range(sample_size):
        card_one = card_generator.get()
        card_two = card_generator.get()
        hand = determine_hand(card_one, card_two)
        simulated_start_hands[hand] = simulated_start_hands.get(hand, 0) + 1

    for key in simulated_start_hands.keys():
        simulated_start_hands[key] = simulated_start_hands[key] / sample_size

    print(f"Montecarlo start hands weights sum: {sum(simulated_start_hands.values())}")
    for key, value in START_HAND_PROBABILITIES.items():
        determinist_probability = round(value, 6)
        montecarlo_probability = round(simulated_start_hands[key], 6)
        print(
            f"Start hand {key} (determinist / montecarlo):\t\t{determinist_probability} / {montecarlo_probability}"
        )

    for key, value in START_HAND_PROBABILITIES.items():
        # accept 1.5% of error max
        assert 0.985 < value / simulated_start_hands[key] < 1.015
