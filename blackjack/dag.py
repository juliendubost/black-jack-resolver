import copy
import os
from dataclasses import dataclass

import numpy
import numpy as np

from blackjack.values import (
    HandState,
    BANK_STARTING_CARDS,
    BANK_STAND_STATES,
    BANK_STAND_SCORES,
    STATE_TO_SCORE,
    PLAYER_END_STATES,
    PLAYER_STARTING_STATES,
)
from blackjack.compute_arrays import hit_transition_matrix, score_ev

HIT_TRANSITION_MATRIX = hit_transition_matrix()

HERE = os.path.dirname(__file__)
PRECOMPUTED = os.path.join(os.path.dirname(HERE), "precomputed")


@dataclass
class Transition:
    destination_hand_state: HandState
    probability: float


#######################################
# Graph of transitions for bank hands #
#######################################


class BankTransitions:
    """
    Graph of bank states with transitions probabilities
    Example with node ACE


    [ ACE ]  --(p:1/13)--> [ TWO_TWELVE ] --(p:1/13)-->  [ THREE_THIRTEEN ]
                                                                |
                                                             (p:1/13)
                                                                |
             --(p:1/13)-->                               [ FOUR_FOURTEEN ]

    """

    def __init__(self):
        self.transitions = {}  # state: list of Transition instances

    def compute(self, state):
        # stop if the state is final
        if state in BANK_STAND_STATES:
            return
        # get all possible transitions using hit matrix
        for hand_state_index, probability in enumerate(
            HIT_TRANSITION_MATRIX[state.value]
        ):
            if probability:
                # add transition to self.transitions
                next_hand_state = HandState(hand_state_index)
                if self.transitions.get(state) is None:
                    self.transitions[state] = []
                self.transitions[state].append(Transition(next_hand_state, probability))
                # check if next node exists, otherwise create it and expand it
                if self.transitions.get(next_hand_state) is None:
                    self.compute(next_hand_state)

    def evaluate_branch(
        self, state, final_scores_probabilities, transition_probabilities=None
    ):
        """
        recursive function that evaluates all transitions starting from state.
        Function stop when the state is a valid bank stand state
        """
        if transition_probabilities is None:
            transition_probabilities = []
        if state in BANK_STAND_STATES:
            # node is in a stand state, evaluate branch probability
            probability = 1
            for transition_probability in transition_probabilities:
                probability *= transition_probability
            if state not in final_scores_probabilities:
                final_scores_probabilities[state] = probability
            else:
                final_scores_probabilities[state] += probability
            return
        for transition in self.transitions.get(state, []):
            branch_transition_probabilities = copy.deepcopy(transition_probabilities)
            branch_transition_probabilities.append(transition.probability)
            self.evaluate_branch(
                transition.destination_hand_state,
                final_scores_probabilities,
                branch_transition_probabilities,
            )

    def get_final_scores_probabilities(self):
        """
        Return the final scores probabilities for each start states as a dict
        A score refer to 1 or 2 states, i.e score of 17 is SEVENTEEN state or SEVEN_SEVENTEEN state
        dict keys are the bank start cards
        dict values are a dict where key is the finale score and value is the probability

        Here are the values in a tabular view
                ACE       2       3       4       5       6       7       8       9      10
          17    0.13    0.14    0.14    0.13    0.12    0.17    0.37    0.13    0.12    0.11
          18    0.13    0.13    0.13    0.13    0.12    0.11    0.14    0.36    0.12    0.11
          19    0.13    0.13    0.13    0.12    0.12    0.11    0.08    0.13    0.35    0.11
          20    0.13    0.12    0.12    0.12    0.11    0.10    0.08    0.07    0.12    0.34
          21    0.05    0.12    0.11    0.11    0.11    0.10    0.07    0.07    0.06    0.03
          BJ    0.31    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.08
        BUST    0.12    0.35    0.37    0.39    0.41    0.42    0.26    0.24    0.23    0.21
        """
        final_scores_matrix = {}
        for state in self.transitions:
            if state in BANK_STARTING_CARDS:
                final_scores_matrix[state] = {}
                final_states_probabilities = {}
                final_scores_probabilities = {key: 0.0 for key in BANK_STAND_SCORES}
                self.evaluate_branch(state, final_states_probabilities)
                for hand_state, value in final_states_probabilities.items():
                    # aggregate states with the same score to compute score probabilities
                    score = STATE_TO_SCORE[hand_state]
                    final_scores_probabilities[score] += value
                for score, value in final_scores_probabilities.items():
                    final_scores_matrix[state][score] = value

        return final_scores_matrix

    def build(self):
        # build the transitions for each bank start card
        for hand_state in HandState:
            if hand_state in BANK_STARTING_CARDS:
                transitions = self.transitions.get(hand_state)
                if transitions is None:
                    self.compute(hand_state)


####################################
# Class for player graph computation
####################################


class PlayerGraph:
    """
    Player DAG for a specific bank card
    bank_score_probabilities is a dict of bank's final scores probabilities
    e.g: {HandState.TWENTY_ONE: 0.13, ...}
    """

    def __init__(self, bank_card):
        self.transitions = {}  # {state: list of Transition instances}$
        self.stand_evs = {}  # {state : expected value if you stand at this state}
        self.hit_evs = {}  # {state : expected value if you hit at this state}

        # bank score probabilities
        bank_transitions = BankTransitions()
        bank_transitions.build()
        self.bank_final_scores_probabilities = (
            bank_transitions.get_final_scores_probabilities()[bank_card]
        )

    def get_stand_ev(self, hand_state):
        stand_ev = 0.0
        for bank_score, probability in self.bank_final_scores_probabilities.items():
            stand_ev += score_ev(hand_state, bank_score) * probability
        return stand_ev

    def _build_stand_evs(self):
        """
        Compute stand expected value of each state
        """
        # build the transitions for each player start card
        for state in HandState:
            if self.stand_evs.get(state) is None:
                self.stand_evs[state] = self.get_stand_ev(state)
                if state not in PLAYER_END_STATES:
                    for index, probability in enumerate(
                        HIT_TRANSITION_MATRIX[state.value]
                    ):
                        next_hand_state = HandState(index)
                        if self.transitions.get(state) is None:
                            self.transitions[state] = []
                        self.transitions[state].append(
                            Transition(next_hand_state, probability)
                        )

    def _build_hit_evs(self):
        """
        Compute the expected values for a card hit then stand for each states
        """
        for state in HandState:
            hit_ev = 0
            for transition in self.transitions.get(state, []):
                hit_ev += (
                    self.stand_evs[transition.destination_hand_state]
                    * transition.probability
                )
            self.hit_evs[state] = hit_ev

    def build(self):
        self._build_stand_evs()
        self._build_hit_evs()

    def get_max_ev(self, state, probability):
        # TODO finish
        for transition in self.transitions.get(state, []):
            transition_hit_ev = self.hit_evs[transition.destination_hand_state]
            transition_stand_ev = self.stand_evs[transition.destination_hand_state]
            max_ev = max(transition_hit_ev, transition_stand_ev) * probability
            if transition.probability and transition_hit_ev:
                max_ev = max(
                    max_ev,
                    self.get_max_ev(transition.destination_hand_state, probability),
                )
        print(f"get_max_ev for {state} is {max_ev}")
        return max_ev

    def evaluate_branch(self, hand_state, branch_probability=1, max_ev=0, hits=0, ):
        stand_ev = self.get_stand_ev(hand_state)
        if stand_ev > max_ev:
            max_ev = stand_ev
        if hand_state in
            #TODO: finish




    def get_best_move(self, state):
        """
        Return the best move for given state
        """
        next_ev = self.hit_evs[state]  # EV of a single hit  (use case "double")
        # Evaluate the maximum ev reachable from this state using one or more cards draw
        max_ev = self.get_max_ev(state, 1)
        stand_ev = self.stand_evs[state]
        if next_ev > stand_ev:
            if next_ev >= max_ev:
                best_move = "double"
            else:
                best_move = "hit"
        elif max_ev > stand_ev:
            best_move = "hit"
        else:
            best_move = "stand"

        print(f"stand_ev: {stand_ev}")
        print(f"next_ev: {next_ev}")
        print(f"max_ev: {max_ev}")
        print(f"best move: {best_move}")
