import random
import math
from utils.helpers import goal_state, find_blank, swap, heuristic

def simulated_annealing(start_state):
    current_state = [row[:] for row in start_state]
    path = []
    visited = set()

    T = 1000
    T_min = 1.0
    alpha = 0.95
    max_iterations = 1000

    current_h = heuristic(current_state)

    while T > T_min and len(path) < max_iterations:
        if current_state == goal_state:
            return path

        state_tuple = tuple(map(tuple, current_state))
        visited.add(state_tuple)

        x, y = find_blank(current_state)
        neighbors = []
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(current_state, x, y, new_x, new_y)
                neighbors.append((heuristic(new_state), new_state, move, (x, y), (new_x, new_y)))

        if not neighbors:
            break

        new_h, new_state, move, old_pos, new_pos = random.choice(neighbors)
        delta_h = new_h - current_h

        if delta_h < 0:
            current_state = [row[:] for row in new_state]
            current_h = new_h
            path.append((move, old_pos, new_pos))
        else:
            probability = math.exp(-delta_h / T)
            if random.random() < probability:
                current_state = [row[:] for row in new_state]
                current_h = new_h
                path.append((move, old_pos, new_pos))

        T *= alpha

    return path
