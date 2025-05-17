from utils.helpers import goal_state, find_blank
import copy

def get_valid_actions(state):
    x, y = find_blank(state)
    actions = []
    if y + 1 < 3: actions.append(("RIGHT", x, y, x, y + 1))
    if x + 1 < 3: actions.append(("DOWN", x, y, x + 1, y))
    if y - 1 >= 0: actions.append(("LEFT", x, y, x, y - 1))
    if x - 1 >= 0: actions.append(("UP", x, y, x - 1, y))
    return actions

def apply_action(state, action, x, y, new_x, new_y):
    new_state = [row[:] for row in state]
    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    return new_state

def partially_observable_search(belief_state):
    debug_logs = []
    debug_logs.append(f"Initial belief state: {belief_state}")
    
    # Kiểm tra ban đầu: nếu đã có trạng thái đạt đích, dừng ngay
    for state in belief_state:
        if state == goal_state:
            debug_logs.append("Found goal state in initial belief state. Stopping.")
            return [], debug_logs
    
    belief_states = [belief_state]
    action_sequence = []
    
    while belief_states:
        current_belief = belief_states[-1]
        debug_logs.append(f"\nCurrent belief state: {current_belief}")
        
        # Tìm hành động có thể áp dụng
        action_applied = False
        for action, x, y, new_x, new_y in get_valid_actions(current_belief[0]):  # Dựa vào trạng thái đầu tiên
            new_belief = []
            step_action = []
            
            for state in current_belief:
                state_list = [list(row) for row in state]
                valid_actions = [a[0] for a in get_valid_actions(state_list)]
                
                if action in valid_actions:
                    new_state = apply_action(state_list, action, x, y, new_x, new_y)
                    new_belief.append(new_state)
                    step_action.append((action, (x, y), (new_x, new_y)))
                else:
                    new_belief.append(state_list)
                    step_action.append(("NONE", (x, y), (x, y)))
            
            # Kiểm tra nếu bất kỳ trạng thái nào trong niềm tin đạt đích
            goal_reached = False
            for state in new_belief:
                if state == goal_state:
                    debug_logs.append(f"Goal state reached with action {action}: {state}")
                    goal_reached = True
                    break
            
            if goal_reached:
                action_sequence.append(step_action)
                debug_logs.append("Stopping as goal state is reached.")
                return action_sequence, debug_logs
            
            # Nếu không đạt đích, tiếp tục thêm niềm tin mới
            if new_belief != current_belief:
                belief_states.append(new_belief)
                action_sequence.append(step_action)
                action_applied = True
                debug_logs.append(f"Applied action {action}, new belief state: {new_belief}")
                break
        
        if not action_applied:
            debug_logs.append("No further actions can be applied or goal not reachable.")
            break
    
    return action_sequence, debug_logs