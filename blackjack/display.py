from blackjack.values import HandState
from blackjack.values import BANK_STARTING_CARDS, PLAYER_STAND_STATES
import sys


def print_hit_transition_array(array):
    row_labels = [HandState.name for HandState in HandState]
    row_label = "              \t" + "\t".join(row_labels)
    print(row_label)
    for row_index, row in enumerate(array):
        col_label = row_labels[row_index]
        line = f"{col_label}\t" + "\t".join([str(round(col, 6)) for col in row])
        print(line)


def print_stand_array(array):
    row_labels = [bankscore.name for bankscore in BANK_STARTING_CARDS]
    col_labels = [playerscore.name for playerscore in PLAYER_STAND_STATES]
    row_label = "              \t" + "\t".join(row_labels)
    print(row_label)
    for row_index, row in enumerate(array):
        col_label = col_labels[row_index]
        line = f"{col_label}\t" + "\t".join([str(round(col, 6)) for col in row])
        print(line)


def print_array(array, row_labels, col_labels, col_length=13):
    """
    labels should be string with a length less than 13
    """
    sys.stdout.write("".rjust(col_length))
    for row_label in row_labels:
        sys.stdout.write(row_label.rjust(col_length))
    sys.stdout.write("\n")
    sys.stdout.flush()
    for i, row in enumerate(array):
        sys.stdout.write(col_labels[i].rjust(col_length))
        for col in row:
            sys.stdout.write(f"{col:.2f}".rjust(col_length))
        sys.stdout.write("\n")
        sys.stdout.flush()
