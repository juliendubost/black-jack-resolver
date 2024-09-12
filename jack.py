import argparse
import sys

from blackjack import (
    settings,
)  # do not import anything else from blackjack package here


def display_ev(bank_card):
    pg = PlayerGraph(bank_card)
    pg.build()
    print(pg)


def display_best_moves(graph_class):
    """ "
    graph_class: Graph class to use to compute best moved (PlayerGraph or any inherited class)
    """
    best_moves_map = {}

    for bank_card in constants.BANK_STARTING_CARDS:
        graph = graph_class(bank_card)
        graph.build()
        best_moves_map[bank_card] = {}
        for player_state in constants.PLAYER_POSSIBLE_STATES:
            best_moves_map[bank_card][player_state] = graph.get_best_move(player_state)
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write(
        f"Player best move for each bank card (first line) and each state (first column)\n"
    )
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write("\t")
    for bank_card in constants.BANK_STARTING_CARDS:
        sys.stdout.write(f"{str(bank_card)}\t")
    sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    for player_state in constants.PLAYER_HARD_STATES:
        sys.stdout.write(f"{str(player_state)}\t")
        for bank_card in best_moves_map.keys():
            sys.stdout.write(f"{best_moves_map[bank_card][player_state]}\t")
        sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    for player_state in constants.PLAYER_SOFT_STATES:
        sys.stdout.write(f"{str(player_state)}\t")
        for bank_card in best_moves_map.keys():
            sys.stdout.write(f"{best_moves_map[bank_card][player_state]}\t")
        sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    for player_state in constants.PLAYER_PAIRS_STATES:
        sys.stdout.write(f"{str(player_state)}\t")
        for bank_card in best_moves_map.keys():
            sys.stdout.write(f"{best_moves_map[bank_card][player_state]}\t")
        sys.stdout.write("\n")
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write("legend:\n")
    sys.stdout.write(f"\t{constants.MOVE_STAND}: Stand\n")
    sys.stdout.write(f"\t{constants.MOVE_HIT}: Hit\n")
    sys.stdout.write(f"\t{constants.MOVE_SPLIT}: Split\n")
    sys.stdout.write(
        f"\t{constants.MOVE_DOUBLE_ELSE_STAND}: Double if possible else stand\n"
    )
    sys.stdout.write(
        f"\t{constants.MOVE_DOUBLE_ELSE_HIT}: Double if possible else hit\n"
    )
    sys.stdout.write(
        f"\t{constants.MOVE_SURRENDER_ELSE_STAND}: Surrender if possible else stand\n"
    )
    sys.stdout.write(
        f"\t{constants.MOVE_SURRENDER_ELSE_HIT}: Surrender if possible else hit\n"
    )
    sys.stdout.write(
        f"\t{constants.MOVE_SURRENDER_ELSE_SPLIT}: Surrender if possible else split\n"
    )
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )
    sys.stdout.write("Computing strategy expected value ...\r")
    game_ev = round(compute_game_ev(PlayerGraph), 6)
    sys.stdout.write(
        f"Total expected value using this strategy if double, split and surrender are allowed is: {game_ev}\n"
    )
    sys.stdout.write(
        f"(you win a total of {game_ev} every time you do an initial bet of 1)\n"
    )
    sys.stdout.write(
        f"-----------------------------------------------------------------------------------\n"
    )


if __name__ == "__main__":
    epilog = """
    compute and display expected values or best moves for given bank start card.
    
    commands are:\n
      ev_table: display expected values table for given bank card
      best_moves: display best moves instead of expected values table
    """

    parser = argparse.ArgumentParser(
        prog="jack.py", epilog=epilog, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("command", help="one of: best_moves or ev_table")
    parser.add_argument(
        "-card",
        help="needed only after ev_table command, one of: A, 2, 3, 4, 5, 6, 7, 8, 9, F",
    )
    parser.add_argument(
        "--no-peek",
        action="store_true",
        help="disable dealer peeked when start card is a figure or an ace",
    )
    parser.add_argument(
        "--hos",
        action="store_true",
        help="dealer hit on soft 17, default is set to false",
    )
    parser.add_argument(
        "--ace-no-draw",
        action="store_true",
        help="Draw is not allowed after pocket aces split",
    )
    parser.add_argument(
        "--ace-no-bj",
        action="store_true",
        help="Blackjack is not allowed after pocket aces split",
    )
    arguments = parser.parse_args()

    settings.DEALER_HIT_ON_SOFT_17 = arguments.hos
    settings.DEALER_PEEKED = not arguments.no_peek
    settings.SPLIT_ACE_ALLOW_BLACKJACK = not arguments.ace_no_bj
    settings.SPLIT_ACE_ALLOW_DRAW = not arguments.ace_no_draw

    # do imports after settings are set
    from blackjack import constants
    from blackjack.graph import PlayerGraph
    from blackjack.ev import compute_game_ev

    hand_states = {
        "A": constants.HandState.ACE,
        "2": constants.HandState.TWO,
        "3": constants.HandState.THREE,
        "4": constants.HandState.FOUR,
        "5": constants.HandState.FIVE,
        "6": constants.HandState.SIX,
        "7": constants.HandState.SEVEN,
        "8": constants.HandState.EIGHT,
        "9": constants.HandState.NINE,
        "F": constants.HandState.FIGURE,
    }

    if arguments.command == "ev_table":
        if arguments.card not in hand_states:
            sys.stdout.write(
                f"unknown card '{arguments.card}' or no card specified (use -c argument) \n"
            )
            sys.exit(1)

        hand_state = hand_states.get(arguments.card)

        if hand_state is None:
            print(
                f"'{arguments.ev_table}' is an incorrect choice for --ev-table argument"
            )

        display_ev(hand_state)

    elif arguments.command == "best_moves":
        display_best_moves(PlayerGraph)

    else:
        sys.stdout.write(f"unknown command {arguments.command}\n")
        sys.exit(1)
