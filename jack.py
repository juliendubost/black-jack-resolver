import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="one of: strategy, evs")
    parser.parse_args()
