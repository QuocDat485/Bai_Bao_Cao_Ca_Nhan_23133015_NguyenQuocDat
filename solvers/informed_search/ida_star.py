from utils.helpers import goal_state, find_blank, swap, heuristic

def ida_star(start_state):
    def search(state, path, g, threshold):
        f = g + heuristic(state)
        if f > threshold:
            return f, None
        if state == goal_state:
            return g, path
        min_cost = float('inf')
        x, y = find_blank(state)
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(state, x, y, new_x, new_y)
                result, found_path = search(new_state, path + [(move, (x, y), (new_x, new_y))], g + 1, threshold)
                if found_path is not None:
                    return result, found_path
                min_cost = min(min_cost, result)
        return min_cost, None

    threshold = heuristic(start_state)
    while True:
        result, path = search(start_state, [], 0, threshold)
        if path is not None:
            return path
        if result == float('inf'):
            return []
        threshold = result
