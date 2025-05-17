from utils.helpers import goal_state, find_blank, swap, heuristic

def steepest_ascent(start_state):
    current_state = [row[:] for row in start_state]
    path = []
    visited = set()

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
                neighbors.append((heuristic(new_state), new_state, move, (x, y), (new_x, new_y)))

        if not neighbors:
            break

        neighbors.sort(key=lambda x: x[0])
        best_heuristic, best_state, best_move, old_pos, new_pos = neighbors[0]

        if best_heuristic < current_h:
            current_state = [row[:] for row in best_state]
            path.append((best_move, old_pos, new_pos))
        else:
            break

    return path
