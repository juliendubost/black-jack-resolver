import argparse
from blackjack.constants import HandState
from blackjack.graph import PlayerGraph


def display_ev(bank_card):
    pg = PlayerGraph(bank_card)
    pg.build()
    print(pg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="jack.py",
        description="compute and display expected values and best move for given bank start card",
    )
    parser.add_argument("bank_card", help="one of: A, 2, 3, 4, 5, 6, 7, 8, 9, F")
    arguments = parser.parse_args()

    hand_states = {
        "A": HandState.ACE,
        "2": HandState.TWO,
        "3": HandState.THREE,
        "4": HandState.FOUR,
        "5": HandState.FIVE,
        "6": HandState.SIX,
        "7": HandState.SEVEN,
        "8": HandState.EIGHT,
        "9": HandState.NINE,
        "F": HandState.FIGURE,
    }

    hand_state = hand_states.get(arguments.bank_card)

    if hand_state is None:
        print(f"'{arguments.bank_card}' is an incorrect choice for bank_card argument")

    display_ev(hand_state)
