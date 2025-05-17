import heapq
from utils.helpers import goal_state, find_blank, swap, heuristic

def a_star(start_state):
    pq = [(heuristic(start_state), 0, start_state, [])]  # (f, g, state, path)
    visited = {}
    while pq:
        f, g, current_state, path = heapq.heappop(pq)
        if current_state == goal_state:
            return path
        state_tuple = tuple(map(tuple, current_state))
        if state_tuple in visited and visited[state_tuple] <= g:
            continue
        visited[state_tuple] = g
        x, y = find_blank(current_state)
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(current_state, x, y, new_x, new_y)
                new_tuple = tuple(map(tuple, new_state))
                if new_tuple not in visited or visited[new_tuple] > g + 1:
                    heapq.heappush(pq, (g + 1 + heuristic(new_state), g + 1, new_state, path + [(move, (x, y), (new_x, new_y))]))
    return []
