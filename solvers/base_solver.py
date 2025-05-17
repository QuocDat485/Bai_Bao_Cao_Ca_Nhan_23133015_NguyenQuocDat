
from solvers.uninformed_search.bfs import bfs
from solvers.uninformed_search.dfs import dfs
from solvers.uninformed_search.ids import ids
from solvers.uninformed_search.ucs import ucs
from solvers.informed_search.greedy import greedy
from solvers.informed_search.a_star import a_star
from solvers.informed_search.ida_star import ida_star
from solvers.local_search.hill_climbing import hill_climbing
from solvers.local_search.steepest_ascent import steepest_ascent
from solvers.local_search.stochastic_hill import stochastic_hill_climbing
from solvers.local_search.simulated_annealing import simulated_annealing
from solvers.local_search.genetic import genetic_algorithm
from solvers.local_search.beam_search import beam_search
from solvers.complex_environments.partially_observable import partially_observable_search
from solvers.CSPs.backtracking import backtracking
from solvers.CSPs.backtracking_fc import backtracking_with_forward_checking
from solvers.complex_environments.and_or_search import and_or_search
# from solvers.complex_environments.belief_state import belief_state_search
# from solvers.complex_environments.partically_observation import sensorless_belief_state_search
from solvers.reinforcement_learning.q_learning import q_learning

class PuzzleSolver:
    def __init__(self, start_state, method):
        self.start_state = start_state
        self.method = method

    def solve(self):
        if self.method == "BFS":
            return bfs(self.start_state)
        elif self.method == "DFS":
            return dfs(self.start_state)
        elif self.method == "IDS":
            return ids(self.start_state)
        elif self.method == "UCS":
            return ucs(self.start_state)
        elif self.method == "Greedy":
            return greedy(self.start_state)
        elif self.method == "A*":
            return a_star(self.start_state)
        elif self.method == "IDA*":
            return ida_star(self.start_state)
        elif self.method == "Hill Climbing":
            return hill_climbing(self.start_state)
        elif self.method == "Steepest Ascent":
            return steepest_ascent(self.start_state)
        elif self.method == "Stochastic Hill":
            return stochastic_hill_climbing(self.start_state)
        elif self.method == "Simulated Annealing":
            return simulated_annealing(self.start_state)
        elif self.method == "Beam Search":
            return beam_search(self.start_state)
        elif self.method == "AND - OR Search":
             return and_or_search(self.start_state)
        elif self.method == "Genetic":
            return genetic_algorithm(self.start_state)
        elif self.method == "Partially Observable Search":
            return partially_observable_search(self.start_state)
        # elif self.method == "Belief State Search":
        #     return belief_state_search(self.start_state)
        elif self.method == "Backtracking":
            return backtracking(self.start_state)
        elif self.method == "Backtracking with Forward Checking":
             return backtracking_with_forward_checking(self.start_state)
        # elif self.method == "Sensorless Belief State Search":
        #     return sensorless_belief_state_search(self.start_state)
        # elif self.method == "Component Problem A*":
        #     return component_problem_a_star(self.start_state)
        elif self.method == "Q_Learning":
            return q_learning(self.start_state)
        return []