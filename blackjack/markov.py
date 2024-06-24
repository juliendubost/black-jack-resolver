from blackjack.compute_arrays import hit_transition_matrix
from blackjack.values import HandState, HandScore

HIT_TRANSITION_MATRIX = hit_transition_matrix()


class ActionNodeMap:
    def __init__(self):
        self.map = {}


class ActionNode:
    """
    Represent a node of the markov's chain for the bank's action graph
    """

    def __str__(self):
        return f"{self.state.name}: {self.branch_ratio}"

    def __repr__(self):
        return f"{self.state.name}: {self.branch_ratio}"

    def __sum__(self):
        return sum(node.branch_ratio for node in self.nodes)

    def __init__(self, hand_state, action_node_map, branch_ratio=1):
        self.nodes = []  # all possible transition nodes with their probabilities
        self.branch_ratio = branch_ratio
        self.action_node_map = (
            action_node_map  # keep track of existing nodes to avoid duplicates
        )
        self.state = hand_state

    def stop(self):
        raise NotImplementedError

    def walk(self):
        raise NotImplementedError


class BankActionNode(ActionNode):
    def stop(self):
        """
        check if the walk should be stopped (if bank score is burned or betweens 17 and 21
        """
        if self.state in [
            HandState.BUST,
            HandState.SEVENTEEN,
            HandState.EIGHTEEN,
            HandState.NINETEEN,
            HandState.TWENTY,
            HandState.TWENTY_ONE,
            HandState.BLACKJACK,
            HandState.SEVEN_SEVENTEEN,
            HandState.EIGHT_EIGHTEEN,
            HandState.NINE_NINETEEN,
            HandState.TEN_TWENTY,
        ]:
            return True
        return False

    def walk(self):
        """
        populate self.nodes with all possible hit transitions
        provided results are not normalised since we count the transistions probabilities to state that are not
        final, i.e TWO_TWELVE
        """
        self.action_node_map[self.state] = self
        if self.stop():
            return
        for col, available_score_probability in enumerate(
                HIT_TRANSITION_MATRIX[self.state.value]
        ):
            if available_score_probability:
                state = HandState(col)
                node = self.action_node_map.get(state)
                if node is not None:
                    node.branch_ratio += self.branch_ratio * available_score_probability
                else:
                    node = BankActionNode(
                        state,
                        self.action_node_map,
                        self.branch_ratio * available_score_probability,
                    )
                    node.walk()
                self.nodes.append(node)


class PlayerActionNode:
    pass
