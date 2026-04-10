import copy
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
    BANK_STARTING_CARDS,
)
from blackjack import settings

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
        self.cards = self.cards * 7  # 7 decks
        self.sysrandom.shuffle(self.cards)

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
        filepath=None,
        bank_hit_on_soft=False,
    ):
        self.card_generator = CardGenerator()
        self.filepath = filepath
        self.hit_on_soft = bank_hit_on_soft
        self.best_moves_map = best_moves_map
        self.exit = False

        # key: start state, value: tuple(expected value, sample size)
        if self.filepath:
            self.ev = json.load(open(self.filepath, "r"))
            LOG.info(f"loaded file {self.filepath}")
        else:
            self.filepath = f"{uuid.uuid4()}.json"
            self.ev = {}
            # use str for consistence with loaded files
            ev_pattern = {
                str(HandState.FIVE): [0, 0],
                str(HandState.SIX): [0, 0],
                str(HandState.SEVEN): [0, 0],
                str(HandState.EIGHT): [0, 0],
                str(HandState.NINE): [0, 0],
                str(HandState.TEN): [0, 0],
                str(HandState.ELEVEN): [0, 0],
                str(HandState.TWELVE): [0, 0],
                str(HandState.THIRTEEN): [0, 0],
                str(HandState.FOURTEEN): [0, 0],
                str(HandState.FIFTEEN): [0, 0],
                str(HandState.SIXTEEN): [0, 0],
                str(HandState.SEVENTEEN): [0, 0],
                str(HandState.EIGHTEEN): [0, 0],
                str(HandState.NINETEEN): [0, 0],
                # str(HandState.TWENTY is excluded, it is considered as a pocket figures,
                str(HandState.BLACKJACK): [0, 0],
                str(HandState.POCKET_ACE): [0, 0],
                str(HandState.POCKET_TWO): [0, 0],
                str(HandState.POCKET_THREE): [0, 0],
                str(HandState.POCKET_FOUR): [0, 0],
                str(HandState.POCKET_FIVE): [0, 0],
                str(HandState.POCKET_SIX): [0, 0],
                str(HandState.POCKET_SEVEN): [0, 0],
                str(HandState.POCKET_EIGHT): [0, 0],
                str(HandState.POCKET_NINE): [0, 0],
                str(HandState.POCKET_FIGURE): [0, 0],
                # str(HandState.TWO_TWELVE is excluded, it is considered as a pocket A
                str(HandState.THREE_THIRTEEN): [0, 0],
                str(HandState.FOUR_FOURTEEN): [0, 0],
                str(HandState.FIVE_FIFTEEN): [0, 0],
                str(HandState.SIX_SIXTEEN): [0, 0],
                str(HandState.SEVEN_SEVENTEEN): [0, 0],
                str(HandState.EIGHT_EIGHTEEN): [0, 0],
                str(HandState.NINE_NINETEEN): [0, 0],
                str(HandState.TEN_TWENTY): [0, 0],
            }
            for card in BANK_STARTING_CARDS:
                self.ev[str(card)] = copy.deepcopy(ev_pattern)

    def random_bank_start_hand(self):
        return self.card_generator.get()

    def random_player_start_hand(self):
        card_one = self.card_generator.get()
        card_two = self.card_generator.get()

        return WEIGHT_TO_HAND[CARD_WEIGHT[card_one] | CARD_WEIGHT[card_two]]

    def get_bank_final_state(self, initial_state):
        """
        Given an initial state, return a final bank state using random cards
        Hit cards until bank state is final
        """
        state = initial_state
        while STATE_TO_SCORE[state] not in BANK_STAND_SCORES:
            state = HIT_TRANSITIONS[state].get(
                self.card_generator.get(), HandState.BUST
            )

        return state

    def total_value(self):
        """
        Return total expected value from simulation
        """
        total_ev = 0
        total_samples = 0
        for bank_card, ev in self.ev.items():
            for value, sample_size in ev.values():
                total_ev += value
                total_samples += sample_size

        LOG.info(f"Total samples: {total_samples}")
        LOG.info(f"Total value: {total_ev}")
        average_per_hand = (1 - total_ev) / total_samples
        LOG.info(f"Average value per hand: {average_per_hand}")
        LOG.info(f"Game EV: {1 + average_per_hand}")

        return total_ev / total_samples

    def save(self):
        """
        Save the simulation result to a unique file
        """
        json.dump(self.ev, open(self.filepath, "w"), indent=2)
        LOG.info(f"Simulation saved to {self.filepath}")
        self.total_value()

    def player_final_states(self, bank_state, player_state, states, deepth=0):
        """
        Recursive method that return states after all moves are done (draws, surrender, splits)
        Only 1 split allowed, surrender is allowed, double is allowed
        Split aces does not allow black jacks (21 instead)
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
                if deepth:
                    if first_hand_state == HandState.BLACKJACK:
                        first_hand_state = HandState.TWENTY_ONE
                    if second_hand_state == HandState.BLACKJACK:
                        second_hand_state = HandState.TWENTY_ONE
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
            else:
                raise ValueError(f"invalid move {best_move}")

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

        bank_final_score = STATE_TO_SCORE[self.get_bank_final_state(bank_initial_state)]
        LOG.debug(f"bank initial: {bank_initial_state}, player initial: {player_initial_state}, bank final score: {bank_final_score}, player final states: {states}")

        total_bet = 0
        total_earn = 0

        for hand_state, bet in states:
            hand_score = STATE_TO_SCORE[hand_state] if hand_state is not None else None
            if hand_score is None:
                # surrendered
                total_bet += 1
                total_earn += 0.5
            elif hand_score == HandState.BUST:
                total_bet += bet
            elif hand_score == HandState.BLACKJACK:
                total_bet += bet
                if bank_final_score == HandState.BLACKJACK:
                    total_earn += bet
                else:
                    total_earn += 2.5
            else:
                total_bet += bet
                if hand_score == bank_final_score:
                    total_earn += bet
                elif hand_score.value > bank_final_score.value:
                    total_earn += 2 * bet

        self.ev[str(bank_initial_state)][str(player_initial_state)][0] += (
            total_earn - total_bet
        )
        self.ev[str(bank_initial_state)][str(player_initial_state)][1] += 1

    def run(self):
        """
        Simulate hands until interrupted, then save results
        """
        LOG.info("Running simulation, press Ctrl+C to stop and save results")
        while True:
            for i in range(300000):
                self.simulate_hand()
            self.save()
            if self.exit:
                break
