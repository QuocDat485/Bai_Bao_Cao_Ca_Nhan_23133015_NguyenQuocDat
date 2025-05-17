from utils.helpers import goal_state, find_blank, swap

def ids(start_state, max_depth=30):
    def dls(state, path, depth, limit, visited):
        if state == goal_state:
            return path
        if depth >= limit:
            return None
        visited.add(tuple(map(tuple, state)))
        x, y = find_blank(state)
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(state, x, y, new_x, new_y)
                if tuple(map(tuple, new_state)) not in visited:
                    result = dls(new_state, path + [(move, (x, y), (new_x, new_y))], depth + 1, limit, visited)
                    if result:
                        return result
        return None

    for depth_limit in range(max_depth):
        visited = set()
        result = dls(start_state, [], 0, depth_limit, visited)
        if result:
            return result
    return []
