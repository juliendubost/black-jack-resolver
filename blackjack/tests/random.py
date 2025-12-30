import datetime
import os
import random
import json
import uuid
import logging

from blackjack.constants import (
    HandState,
    BANK_STAND_SCORES,
    HIT_TRANSITIONS,
    STATE_TO_SCORE,
    CARD_WEIGHT,
    WEIGHT_TO_HAND,
    PLAYER_END_STATES,
    MOVE_SURRENDER_ELSE_STAND,
    MOVE_HIT,
    MOVE_SPLIT,
    MOVE_DOUBLE_ELSE_HIT,
    MOVE_DOUBLE_ELSE_STAND,
    MOVE_STAND,
    MOVE_SURRENDER_ELSE_HIT,
    POST_SPLIT_STATE,
)

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class CardGenerator:
    def __init__(self):
        self.sysrandom = random.SystemRandom()
        self.cards = [
            HandState.ACE,
            HandState.TWO,
            HandState.THREE,
            HandState.FOUR,
            HandState.FIVE,
            HandState.SIX,
            HandState.SEVEN,
            HandState.EIGHT,
            HandState.NINE,
            HandState.FIGURE,  # represent a 10
            HandState.FIGURE,  # represent a jack
            HandState.FIGURE,  # represent a queen
            HandState.FIGURE,  # represent a king
        ]

    def get(self):
        """
        Get a random card from self.cards
        """
        return self.sysrandom.choice(self.cards)


def get_bank_score(initial_state, card_generator):
    """
    Given an initial state, return a final bank score using random cards
    Hit cards until bank state is final
    """
    state = initial_state
    while STATE_TO_SCORE[state] not in BANK_STAND_SCORES:
        state = HIT_TRANSITIONS[state].get(card_generator.get(), HandState.BUST)

    return state


class Simulator:
    def __init__(
        self,
        best_moves_map,
        output_dir_path=f"simulations/{datetime.datetime.now().isoformat()}",
        bank_hit_on_soft=False,
    ):
        self.card_generator = CardGenerator()
        self.output_dir_path = output_dir_path
        self.hit_on_soft = bank_hit_on_soft
        self.best_moves_map = best_moves_map

        # key: start state, value: tuple(expected value, sample size)
        self.ev = {
            HandState.FIVE: [0, 0],
            HandState.SIX: [0, 0],
            HandState.SEVEN: [0, 0],
            HandState.EIGHT: [0, 0],
            HandState.NINE: [0, 0],
            HandState.TEN: [0, 0],
            HandState.ELEVEN: [0, 0],
            HandState.TWELVE: [0, 0],
            HandState.THIRTEEN: [0, 0],
            HandState.FOURTEEN: [0, 0],
            HandState.FIFTEEN: [0, 0],
            HandState.SIXTEEN: [0, 0],
            HandState.SEVENTEEN: [0, 0],
            HandState.EIGHTEEN: [0, 0],
            HandState.NINETEEN: [0, 0],
            # HandState.TWENTY is excluded, it is considered as a pocket figures,
            HandState.BLACKJACK: [0, 0],
            HandState.POCKET_ACE: [0, 0],
            HandState.POCKET_TWO: [0, 0],
            HandState.POCKET_THREE: [0, 0],
            HandState.POCKET_FOUR: [0, 0],
            HandState.POCKET_FIVE: [0, 0],
            HandState.POCKET_SIX: [0, 0],
            HandState.POCKET_SEVEN: [0, 0],
            HandState.POCKET_EIGHT: [0, 0],
            HandState.POCKET_NINE: [0, 0],
            HandState.POCKET_FIGURE: [0, 0],
            # HandState.TWO_TWELVE is excluded, it is considered as a pocket A
            HandState.THREE_THIRTEEN: [0, 0],
            HandState.FOUR_FOURTEEN: [0, 0],
            HandState.FIVE_FIFTEEN: [0, 0],
            HandState.SIX_SIXTEEN: [0, 0],
            HandState.SEVEN_SEVENTEEN: [0, 0],
            HandState.EIGHT_EIGHTEEN: [0, 0],
            HandState.NINE_NINETEEN: [0, 0],
            HandState.TEN_TWENTY: [0, 0],
        }

    def random_bank_start_hand(self):
        return self.card_generator.get()

    def random_player_start_hand(self):
        card_one = self.card_generator.get()
        card_two = self.card_generator.get()

        return WEIGHT_TO_HAND[CARD_WEIGHT[card_one] | CARD_WEIGHT[card_two]]

    def get_bank_score(self, initial_state):
        """
        Given an initial state, return a final bank score using random cards
        Hit cards until bank state is final
        """
        state = initial_state
        while STATE_TO_SCORE[state] not in BANK_STAND_SCORES:
            state = HIT_TRANSITIONS[state].get(
                self.card_generator.get(), HandState.BUST
            )

        return state

    def save(self):
        """
        Save the simulation result to a unique file
        """
        filepath = os.path.join(self.output_dir_path, f"{str(uuid.uuid4())}.json")
        json.dump(self.ev, open(filepath, "w"), indent=2)

    def player_final_states(self, bank_state, player_state, states, deepth=0):
        """
        Recursive method that return states after all moves are done (draws, surrender, splits)
        Only 1 split allowed, surrender is allowed, double is allowed
        states: list of tuples (HandState, bet integer)
        """

        hit = False
        initial_state = player_state  # used only for logging

        while player_state not in PLAYER_END_STATES:
            best_move = self.best_moves_map[bank_state][player_state]
            if best_move in [MOVE_SURRENDER_ELSE_STAND, MOVE_SURRENDER_ELSE_HIT]:
                if deepth == 0:
                    # surrender is allowed
                    LOG.debug(
                        f"bank: {bank_state}, player: {initial_state}] => surrender"
                    )
                    states.append((None, 0.5))
                    break
                elif best_move == MOVE_SURRENDER_ELSE_HIT:
                    # can't surrender since it's a split hand
                    player_state = HIT_TRANSITIONS[player_state].get(
                        self.card_generator.get(), HandState.BUST
                    )
                    LOG.debug(
                        f"bank: {bank_state}, player: {initial_state}] => hit to {player_state}"
                    )
                    hit = True
                else:
                    # surrender else stand case so it's a stand
                    states.append((player_state, 1))
                    LOG.debug(f"bank: {bank_state}, player: {initial_state}] => stand")
                    break
            elif best_move == MOVE_STAND:
                states.append((player_state, 1))
                LOG.debug(f"bank: {bank_state}, player: {initial_state}] => stand")
                break
            elif best_move == MOVE_HIT:
                player_state = HIT_TRANSITIONS[player_state].get(
                    self.card_generator.get(), HandState.BUST
                )
                LOG.debug(
                    f"bank: {bank_state}, player: {initial_state}] => hit to {player_state}"
                )
                initial_state = player_state
            elif best_move == MOVE_SPLIT:
                first_hand_state = HIT_TRANSITIONS[POST_SPLIT_STATE[player_state]][
                    self.card_generator.get()
                ]
                second_hand_state = HIT_TRANSITIONS[POST_SPLIT_STATE[player_state]][
                    self.card_generator.get()
                ]
                LOG.debug(
                    f"bank: {bank_state}, player: {initial_state}] => split to {first_hand_state} & {second_hand_state}"
                )
                self.player_final_states(
                    bank_state, first_hand_state, states, deepth + 1
                )
                self.player_final_states(
                    bank_state, second_hand_state, states, deepth + 1
                )
                break
            elif best_move == MOVE_DOUBLE_ELSE_HIT:
                # hit anyway
                player_state = HIT_TRANSITIONS[player_state].get(
                    self.card_generator.get(), HandState.BUST
                )
                if not hit:
                    # can double, so double bet and break
                    states.append((player_state, 2))
                    LOG.debug(
                        f"bank: {bank_state}, player: {initial_state}] => double to {player_state}"
                    )
                    break
                LOG.debug(
                    f"bank: {bank_state}, player: {initial_state}] => hit to {player_state}"
                )
            elif best_move == MOVE_DOUBLE_ELSE_STAND:
                if not hit:
                    # can double, so double bet and break
                    player_state = HIT_TRANSITIONS[player_state].get(
                        self.card_generator.get(), HandState.BUST
                    )
                    states.append((player_state, 2))
                    LOG.debug(
                        f"bank: {bank_state}, player: {initial_state}] => double to {player_state}"
                    )
                else:
                    # stand
                    states.append((player_state, 1))
                    LOG.debug(f"bank: {bank_state}, player: {initial_state}] => stand")
                break

    def simulate_hand(self, player_initial_state=None, bank_initial_state=None):
        """
        Simulate a hand and return value
        """
        if player_initial_state is None:
            player_initial_state = self.random_player_start_hand()
        if bank_initial_state is None:
            bank_initial_state = self.random_bank_start_hand()

        states = []
        self.player_final_states(bank_initial_state, player_initial_state, states)

        # TODO: make evaluation againt bank card and save values
        