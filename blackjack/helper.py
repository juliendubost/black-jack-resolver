from blackjack import display
from blackjack import values
from blackjack import dag

# compute bank final scores probabilities
bank_transitions = dag.BankTransitions()
bank_transitions.build()
final_scores_probabilities = bank_transitions.get_final_scores_probabilities()

# Compute stand expected value
player_graph = dag.PlayerGraph()
