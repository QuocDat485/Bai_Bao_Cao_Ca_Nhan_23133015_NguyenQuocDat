goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def find_blank(state):
    # Đảm bảo state là list
    state_list = [list(row) for row in state]
    for i in range(3):
        for j in range(3):
            if state_list[i][j] == 0:
                return i, j
    return None

def swap(state, x1, y1, x2, y2):
    # Đảm bảo state là list (fix lỗi tuple)
    new_state = [list(row) for row in state]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

def heuristic(state):
    # Đảm bảo state là list
    state_list = [list(row) for row in state]
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state_list[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // 3, (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def is_solvable(state):
    # Đảm bảo state là list
    state_list = [list(row) for row in state]
    flat_state = [num for row in state_list for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
    return inversions % 2 == 0