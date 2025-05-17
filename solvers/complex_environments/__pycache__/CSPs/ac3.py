from utils.helpers import goal_state, find_blank

def ac3(belief_state, debug_logs=None):
    if debug_logs is None:
        debug_logs = []
    
    debug_logs.append(f"AC-3: Bắt đầu với {len(belief_state)} trạng thái trong belief state.")
    
    # Ràng buộc: Mỗi trạng thái phải có các số từ 0-8 duy nhất và hợp lệ
    def is_consistent(state):
        flat_state = [num for row in state for num in row]
        # Kiểm tra trùng lặp và hợp lệ
        if len(set(flat_state)) != 9 or not all(0 <= num <= 8 for num in flat_state):
            return False
        # Kiểm tra khả thi (tạm thời bỏ qua tính khả thi liên quan đến goal state)
        return True

    # Lọc các trạng thái không nhất quán
    filtered_belief = []
    for state in belief_state:
        if is_consistent(state):
            filtered_belief.append(state)
        else:
            debug_logs.append(f"AC-3: Loại bỏ trạng thái không nhất quán: {state}")

    if not filtered_belief:
        debug_logs.append("AC-3: Không còn trạng thái nào thỏa mãn ràng buộc.")
        return None

    # Ràng buộc bổ sung: Với sensorless hoặc partially observable, có thể thêm ràng buộc về vị trí số 0
    def propagate_constraints():
        queue = [(state, i, j) for state in filtered_belief for i in range(3) for j in range(3)]
        while queue:
            state, i, j = queue.pop(0)
            if state[i][j] == 0:  # Chỉ kiểm tra ô trống
                x, y = i, j
                valid_moves = []
                if y + 1 < 3: valid_moves.append("RIGHT")
                if x + 1 < 3: valid_moves.append("DOWN")
                if y - 1 >= 0: valid_moves.append("LEFT")
                if x - 1 >= 0: valid_moves.append("UP")
                # Đảm bảo trạng thái có ít nhất một hành động hợp lệ
                if not valid_moves:
                    debug_logs.append(f"AC-3: Loại bỏ trạng thái không có hành động hợp lệ: {state}")
                    filtered_belief.remove(state)
    
    propagate_constraints()
    
    if not filtered_belief:
        debug_logs.append("AC-3: Không còn trạng thái nào sau khi lan truyền ràng buộc.")
        return None

    debug_logs.append(f"AC-3: Kết thúc với {len(filtered_belief)} trạng thái sau khi lọc.")
    return filtered_belief
