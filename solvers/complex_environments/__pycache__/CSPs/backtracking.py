from utils.helpers import goal_state, find_blank, swap

def backtracking(start_state, max_depth=50):
    def backtrack(state, path, depth, visited):
        if state == goal_state:
            return path
        if depth >= max_depth:
            return None
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            return None
        visited.add(state_tuple)

        x, y = find_blank(state)
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(state, x, y, new_x, new_y)
                result = backtrack(new_state, path + [(move, (x, y), (new_x, new_y))], depth + 1, visited)
                if result is not None:
                    return result
        return None

    visited = set()
    result = backtrack(start_state, [], 0, visited)
    return result if result is not None else []