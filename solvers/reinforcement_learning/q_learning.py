import random
import numpy as np
import pickle
import os
from utils.helpers import goal_state, find_blank, swap, heuristic

def q_learning(start_state, episodes=10000, max_steps=500, alpha=0.1, gamma=0.9, epsilon=0.5):
    """
    Thuật toán Q-Learning cho bài toán 8-Puzzle.
    - episodes: Số lượng tập huấn luyện
    - max_steps: Số bước tối đa mỗi tập
    - alpha: Tốc độ học
    - gamma: Hệ số chiết khấu cho phần thưởng tương lai
    - epsilon: Tỷ lệ khám phá cho chính sách epsilon-greedy
    """
    # Tệp lưu bảng Q
    q_table_file = "q_table.pkl"

    # Khởi tạo bảng Q
    q_table = {}
    actions = ["RIGHT", "DOWN", "LEFT", "UP"]

    # Nạp bảng Q nếu đã tồn tại
    if os.path.exists(q_table_file):
        with open(q_table_file, "rb") as f:
            q_table = pickle.load(f)
        print("Đã nạp bảng Q từ tệp!")

    def get_valid_actions(state):
        # Lấy danh sách các hành động hợp lệ từ trạng thái hiện tại
        x, y = find_blank(state)
        valid_actions = []
        if y + 1 < 3:
            valid_actions.append("RIGHT")
        if x + 1 < 3:
            valid_actions.append("DOWN")
        if y - 1 >= 0:
            valid_actions.append("LEFT")
        if x - 1 >= 0:
            valid_actions.append("UP")
        return valid_actions

    def get_next_state(state, action):
        # Thực hiện hành động và trả về trạng thái mới cùng vị trí ô trống
        x, y = find_blank(state)
        if action == "RIGHT" and y + 1 < 3:
            return swap(state, x, y, x, y + 1), (x, y), (x, y + 1)
        elif action == "DOWN" and x + 1 < 3:
            return swap(state, x, y, x + 1, y), (x, y), (x + 1, y)
        elif action == "LEFT" and y - 1 >= 0:
            return swap(state, x, y, x, y - 1), (x, y), (x, y - 1)
        elif action == "UP" and x - 1 >= 0:
            return swap(state, x, y, x - 1, y), (x, y), (x - 1, y)
        return state, (x, y), (x, y)  # Hành động không hợp lệ, trạng thái không đổi

    def get_reward(state, next_state):
        # Tính phần thưởng dựa trên trạng thái mới
        if next_state == goal_state:
            return 200  # Phần thưởng lớn hơn nếu đạt trạng thái đích
        if next_state == state:  # Di chuyển không hợp lệ
            return -20  # Phạt nặng hơn cho hành động không hợp lệ
        # Thêm heuristic để hướng dẫn học
        manhattan_distance = heuristic(next_state)
        return -1 - manhattan_distance * 0.5  # Tăng trọng số heuristic

    def generate_random_state(base_state):
        # Tạo trạng thái ngẫu nhiên bằng cách di chuyển ngẫu nhiên từ trạng thái cơ sở
        state = [row[:] for row in base_state]
        for _ in range(10):  # Thực hiện 10 di chuyển ngẫu nhiên
            valid_actions = get_valid_actions(state)
            if not valid_actions:
                break
            action = random.choice(valid_actions)
            state, _, _ = get_next_state(state, action)
        return state

    # Giai đoạn huấn luyện
    for episode in range(episodes):
        # Thay đổi trạng thái ban đầu ngẫu nhiên mỗi 100 tập
        if episode % 100 == 0:
            state = generate_random_state(start_state)
        else:
            state = [row[:] for row in start_state]
        state_tuple = tuple(map(tuple, state))

        for step in range(max_steps):
            if state == goal_state:
                break  # Thoát nếu đạt trạng thái đích

            # Chọn hành động theo chính sách epsilon-greedy
            valid_actions = get_valid_actions(state)
            if not valid_actions:
                break

            if random.random() < epsilon:
                action = random.choice(valid_actions)  # Khám phá: chọn ngẫu nhiên
            else:
                # Khởi tạo giá trị Q cho trạng thái nếu chưa có
                if state_tuple not in q_table:
                    q_table[state_tuple] = {a: 0.0 for a in actions}
                # Khai thác: chọn hành động có giá trị Q cao nhất
                q_values = q_table[state_tuple]
                action = max(valid_actions, key=lambda a: q_values[a])

            # Thực hiện hành động
            next_state, old_pos, new_pos = get_next_state(state, action)
            next_state_tuple = tuple(map(tuple, next_state))

            # Tính phần thưởng
            reward = get_reward(state, next_state)

            # Cập nhật bảng Q
            if state_tuple not in q_table:
                q_table[state_tuple] = {a: 0.0 for a in actions}
            if next_state_tuple not in q_table:
                q_table[next_state_tuple] = {a: 0.0 for a in actions}

            current_q = q_table[state_tuple][action]
            next_max_q = max(q_table[next_state_tuple].values())
            q_table[state_tuple][action] = current_q + alpha * (reward + gamma * next_max_q - current_q)

            # Chuyển sang trạng thái mới
            state = [row[:] for row in next_state]
            state_tuple = next_state_tuple

        # Giảm epsilon để giảm khám phá theo thời gian
        epsilon = max(0.01, epsilon * 0.99)

        # In tiến trình huấn luyện
        if (episode + 1) % 1000 == 0:
            print(f"Đã hoàn thành {episode + 1}/{episodes} tập huấn luyện")

    # Lưu bảng Q vào tệp
    with open(q_table_file, "wb") as f:
        pickle.dump(q_table, f)
    print("Đã lưu bảng Q vào tệp!")

    # Giai đoạn trích xuất đường đi
    path = []
    state = [row[:] for row in start_state]
    state_tuple = tuple(map(tuple, state))
    visited = set()
    max_steps_policy = 500  # Tăng giới hạn để tìm đường đi dài

    for step in range(max_steps_policy):
        if state == goal_state:
            print("Đã đạt trạng thái đích!")
            break  # Thoát nếu đạt trạng thái đích
        if state_tuple in visited:
            print("Gặp vòng lặp tại trạng thái:", state)
            break  # Tránh lặp lại trạng thái
        visited.add(state_tuple)

        # Chọn hành động tốt nhất dựa trên bảng Q
        valid_actions = get_valid_actions(state)
        if not valid_actions:
            print("Không có hành động hợp lệ tại trạng thái:", state)
            break

        if state_tuple not in q_table:
            # Nếu trạng thái chưa học, chọn ngẫu nhiên
            print("Trạng thái chưa học:", state)
            action = random.choice(valid_actions)
        else:
            q_values = q_table[state_tuple]
            action = max(valid_actions, key=lambda a: q_values[a])

        # Thực hiện hành động
        next_state, old_pos, new_pos = get_next_state(state, action)
        path.append((action, old_pos, new_pos))
        print(f"Bước {step + 1}: Hành động {action}, Trạng thái mới:", next_state)

        # Chuyển sang trạng thái mới
        state = [row[:] for row in next_state]
        state_tuple = tuple(map(tuple, state))

    if state != goal_state:
        print("Không đạt trạng thái đích. Trạng thái cuối:", state)

    return path