import random
from utils.helpers import goal_state, find_blank, swap, heuristic

def stochastic_hill_climbing(start_state):
    current_state = [row[:] for row in start_state]
    path = []
    visited = set()
    max_stagnation = 5

    while current_state != goal_state:
        state_tuple = tuple(map(tuple, current_state))
        if state_tuple in visited:
            break
        visited.add(state_tuple)

        x, y = find_blank(current_state)
        neighbors = []
        current_h = heuristic(current_state)

        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(current_state, x, y, new_x, new_y)
                h = heuristic(new_state)
                if h < current_h:
                    neighbors.append((h, new_state, move, (x, y), (new_x, new_y)))

        if not neighbors:
            if len(path) < max_stagnation:
                all_neighbors = []
                for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < 3 and 0 <= new_y < 3:
                        new_state = swap(current_state, x, y, new_x, new_y)
                        all_neighbors.append((heuristic(new_state), new_state, move, (x, y), (new_x, new_y)))
                if all_neighbors:
                    _, next_state, next_move, old_pos, new_pos = random.choice(all_neighbors)
                    current_state = [row[:] for row in next_state]
                    path.append((next_move, old_pos, new_pos))
                    continue
            break

        _, next_state, next_move, old_pos, new_pos = random.choice(neighbors)
        current_state = [row[:] for row in next_state]
        path.append((next_move, old_pos, new_pos))

    return path
