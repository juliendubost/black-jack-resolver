import argparse
import sys

from blackjack.constants import (
    HandState,
    BANK_STARTING_CARDS,
    PLAYER_HARD_STATES,
    PLAYER_SOFT_STATES,
    PLAYER_PAIRS_STATES,
    PLAYER_POSSIBLE_STATES,
    MOVE_STAND,
    MOVE_SPLIT,
    MOVE_DOUBLE_ELSE_STAND,
    MOVE_DOUBLE_ELSE_HIT,
    MOVE_SURRENDER_ELSE_SPLIT,
    MOVE_SURRENDER_ELSE_HIT,
    MOVE_SURRENDER_ELSE_STAND,
    MOVE_HIT,
    MOVE_DOUBLE,
)
from blackjack.graph import PlayerGraph
from blackjack.ev import compute_game_ev


def display_ev(bank_card):
    pg = PlayerGraph(bank_card)
    pg.build()
    print(pg)


def display_best_moves():
    best_moves_map = {}

    for bank_card in BANK_STARTING_CARDS:
        player_graph = PlayerGraph(bank_card)
        player_graph.build()
        best_moves_map[bank_card] = {}
        for player_state in PLAYER_POSSIBLE_STATES:
            best_moves_map[bank_card][player_state] = player_graph.get_best_move(
                player_state
            )
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write(
        f"Player best move for each bank card (first line) and each state (first column)\n"
    )
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write(f"\t2\t3\t4\t5\t6\t7\t8\t9\t10\tA\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    for player_state in PLAYER_HARD_STATES:
        sys.stdout.write(f"{str(player_state)}\t")
        for bank_card in best_moves_map.keys():
            sys.stdout.write(f"{best_moves_map[bank_card][player_state]}\t")
        sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    for player_state in PLAYER_SOFT_STATES:
        sys.stdout.write(f"{str(player_state)}\t")
        for bank_card in best_moves_map.keys():
            sys.stdout.write(f"{best_moves_map[bank_card][player_state]}\t")
        sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    for player_state in PLAYER_PAIRS_STATES:
        sys.stdout.write(f"{str(player_state)}\t")
        for bank_card in best_moves_map.keys():
            sys.stdout.write(f"{best_moves_map[bank_card][player_state]}\t")
        sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write("legend:\n")
    sys.stdout.write(f"\t{MOVE_STAND}: Stand\n")
    sys.stdout.write(f"\t{MOVE_HIT}: Hit\n")
    sys.stdout.write(f"\t{MOVE_SPLIT}: Split\n")
    sys.stdout.write(f"\t{MOVE_DOUBLE_ELSE_STAND}: Double if possible else stand\n")
    sys.stdout.write(f"\t{MOVE_DOUBLE_ELSE_HIT}: Double if possible else hit\n")
    sys.stdout.write(
        f"\t{MOVE_SURRENDER_ELSE_STAND}: Surrender if possible else stand\n"
    )
    sys.stdout.write(f"\t{MOVE_SURRENDER_ELSE_HIT}: Surrender if possible else hit\n")
    sys.stdout.write(
        f"\t{MOVE_SURRENDER_ELSE_SPLIT}: Surrender if possible else split\n"
    )
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write("Computing strategy expected value ...\r")
    game_ev = round(compute_game_ev(PlayerGraph), 6)
    sys.stdout.write(f"Total expected value using this strategy is: {game_ev}\n")
    sys.stdout.write(f"(you win a total of {game_ev} every time you bet 1)\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="jack.py",
        description="compute and display expected values or best moves for given bank start card",
    )
    parser.add_argument(
        "--ev-table",
        help="display expected values table for given bank card: A, 2, 3, 4, 5, 6, 7, 8, 9, F",
    )
    parser.add_argument(
        "--best-moves",
        action="store_true",
        help="display best moves instead of expected values table",
    )
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

    if arguments.ev_table is not None:
        hand_state = hand_states.get(arguments.ev_table)

        if hand_state is None:
            print(
                f"'{arguments.ev_table}' is an incorrect choice for --ev-table argument"
            )

        display_ev(hand_state)

    if arguments.best_moves is True:
        display_best_moves()
