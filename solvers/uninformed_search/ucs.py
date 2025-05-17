
import heapq
from utils.helpers import goal_state, find_blank, swap

def ucs(start_state):
    pq = [(0, start_state, [])]
    visited = set()
    while pq:
        cost, current_state, path = heapq.heappop(pq)
        if current_state == goal_state:
            return path
        visited.add(tuple(map(tuple, current_state)))
        x, y = find_blank(current_state)
        for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(current_state, x, y, new_x, new_y)
                if tuple(map(tuple, new_state)) not in visited:
                    heapq.heappush(pq, (cost + 1, new_state, path + [(move, (x, y), (new_x, new_y))]))
    return []