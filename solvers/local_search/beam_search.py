import heapq
from utils.helpers import goal_state, find_blank, swap, heuristic

def beam_search(start_state, beam_width=2):
    pq = [(heuristic(start_state), start_state, [])]
    visited = set()
    visited.add(tuple(map(tuple, start_state)))

    while pq:
        current_nodes = []
        for _ in range(min(beam_width, len(pq))):
            if not pq:
                break
            h, state, path = heapq.heappop(pq)
            current_nodes.append((h, state, path))

        next_nodes = []
        for _, current_state, path in current_nodes:
            if current_state == goal_state:
                return path

            x, y = find_blank(current_state)
            for dx, dy, move in [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 3 and 0 <= new_y < 3:
                    new_state = swap(current_state, x, y, new_x, new_y)
                    state_tuple = tuple(map(tuple, new_state))
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        h = heuristic(new_state)
                        next_nodes.append((h, new_state, path + [(move, (x, y), (new_x, new_y))]))

        next_nodes.sort(key=lambda x: x[0])
        pq = []
        for i in range(min(beam_width, len(next_nodes))):
            h, state, path = next_nodes[i]
            heapq.heappush(pq, (h, state, path))

    return []