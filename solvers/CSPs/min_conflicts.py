from utils.helpers import goal_state, find_blank, swap, heuristic
import random

def min_conflicts(start_state, max_steps=1000):
    def conflicts(state, x, y, new_x, new_y):
        """Tính số xung đột sau khi hoán đổi ô trống tại (x, y) với ô tại (new_x, new_y)."""
        temp_state = swap(state, x, y, new_x, new_y)
        return heuristic(temp_state)

    current_state = [row[:] for row in start_state]
    path = []

    for step in range(max_steps):
        if current_state == goal_state:
            return path

        # Tìm vị trí ô trống
        x, y = find_blank(current_state)

        # Lấy danh sách các ô liền kề hợp lệ
        directions = [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]
        valid_moves = []
        for dx, dy, move in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                num_conflicts = conflicts(current_state, x, y, new_x, new_y)
                valid_moves.append((num_conflicts, new_x, new_y, move))

        if not valid_moves:
            continue

        # Chọn di chuyển tốt nhất (ít xung đột nhất)
        valid_moves.sort(key=lambda x: x[0])  # Sắp xếp theo số xung đột
        best_conflicts, best_x, best_y, best_move = valid_moves[0]

        # Thực hiện di chuyển tốt nhất
        current_state = swap(current_state, x, y, best_x, best_y)
        path.append((best_move, (x, y), (best_x, best_y)))

    return path if current_state == goal_state else []