from utils.helpers import goal_state, find_blank, swap

def dfs(start_state, max_depth=50):
    stack = [(start_state, [], 0)]
    visited = set()
    while stack:
        current_state, path, depth = stack.pop()
        if current_state == goal_state:
            return path
        if depth >= max_depth:
            continue
        visited.add(tuple(map(tuple, current_state)))
        x, y = find_blank(current_state)
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(current_state, x, y, new_x, new_y)
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    stack.append((new_state, path + [(move, (x, y), (new_x, new_y))], depth + 1))
    return []
