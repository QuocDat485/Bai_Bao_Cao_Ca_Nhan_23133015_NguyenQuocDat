import tkinter as tk
from tkinter import messagebox, ttk
import time
import itertools
from solvers.base_solver import PuzzleSolver
from utils.helpers import goal_state, find_blank

class ComplexEnvironmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver - Complex Environment")
        self.root.geometry("900x650")
        self.root.configure(bg="#2C3E50")
        self.environment = tk.StringVar(value="partially_observable")  # Mặc định là partially observable
        self.method = tk.StringVar(value="BFS")  # Mặc định thuật toán là BFS
        self.initial_belief_state = self.generate_initial_belief()  # Tự động tạo belief state
        self.current_belief_state = [state[:] for state in self.initial_belief_state]
        self.steps = []
        self.current_page = 0
        self.states_per_page = 3
        self.create_widgets()
        self.update_belief_display()
        self.draw_goal_state()

    def generate_initial_belief(self):
        if self.environment.get() == "partially_observable":
            # Belief state mẫu cho môi trường partially observable (biết một phần thông tin)
            return [
                [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
                [[1, 2, 3], [4, 5, 6], [0, 7, 8]],
                [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
            ]
        else:  # Sensorless
            # Sinh 10 trạng thái hợp lệ (không biết trạng thái hiện tại)
            numbers = list(range(9))
            selected_states = []
            for perm in itertools.permutations(numbers):
                state = [list(perm[i:i + 3]) for i in range(0, 9, 3)]
                if self.is_valid_state(state):
                    from utils.helpers import heuristic
                    h = heuristic(state)
                    if 2 <= h <= 4 and state not in selected_states:
                        selected_states.append(state)
                    if len(selected_states) >= 5:  # Lấy đúng 5 trạng thái
                        break
            return selected_states

    def is_valid_state(self, state):
        # Kiểm tra trạng thái có hợp lệ
        flat_state = [num for row in state for num in row]
        return 0 in flat_state and len(set(flat_state)) == 9

    def create_widgets(self):
        # Tiêu đề chính
        title_label = tk.Label(self.root, text="8-Puzzle Solver - Complex Environment", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50")
        title_label.pack(pady=10)

        # Frame chính
        main_frame = tk.Frame(self.root, bg="#E5ECEE", padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Frame bên trái (cho môi trường, belief state, goal state)
        left_frame = tk.Frame(main_frame, bg="#E5ECEE", width=180)
        left_frame.pack(side=tk.LEFT, fill="y", padx=10)
        left_frame.pack_propagate(0)

        # Chọn môi trường (điều chỉnh kích thước và padding)
        env_frame = tk.Frame(left_frame, bg="#D5DBDB", bd=2, relief="groove", padx=5, pady=5)
        env_frame.pack(pady=10, fill="x")
        tk.Label(env_frame, text="Chọn môi trường:", font=("Arial", 12, "bold"), fg="#2C3E50", bg="#D5DBDB").pack(anchor="w", pady=2)
        environments = [("Partially Observable", "partially_observable"), ("Sensorless", "sensorless")]
        for text, value in environments:
            tk.Radiobutton(env_frame, text=text, variable=self.environment, value=value, font=("Arial", 10), fg="#2C3E50", bg="#D5DBDB", command=self.update_environment).pack(anchor="w", padx=5, pady=2)

        # Belief state ban đầu
        tk.Label(left_frame, text="Niềm tin ban đầu", font=("Arial", 10, "bold"), fg="#2C3E50", bg="#E5ECEE").pack(pady=5)
        initial_frame = tk.Frame(left_frame, bg="#E5ECEE")
        initial_frame.pack(fill="both", expand=True)
        self.initial_belief_canvas = tk.Canvas(initial_frame, width=160, height=360, bg="#E5ECEE", highlightthickness=1, highlightbackground="#5DADE2")
        v_scrollbar = ttk.Scrollbar(initial_frame, orient="vertical", command=self.initial_belief_canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.initial_belief_canvas.configure(yscrollcommand=v_scrollbar.set)
        self.initial_belief_inner = tk.Frame(self.initial_belief_canvas, bg="#E5ECEE")
        self.initial_belief_canvas.create_window((0, 0), window=self.initial_belief_inner, anchor="nw")
        self.initial_belief_inner.bind("<Configure>", lambda e: self.initial_belief_canvas.configure(scrollregion=self.initial_belief_canvas.bbox("all")))
        self.initial_belief_canvas.pack(pady=5)

        # Trạng thái đích
        tk.Label(left_frame, text="Trạng thái đích", font=("Arial", 10, "bold"), fg="#2C3E50", bg="#E5ECEE").pack(pady=5)
        self.goal_canvas = tk.Canvas(left_frame, width=160, height=130, bg="#E5ECEE", highlightthickness=1, highlightbackground="#5DADE2")
        self.goal_canvas.pack(pady=5)

        # Frame bên phải (cho quá trình giải)
        right_frame = tk.Frame(main_frame, bg="#E5ECEE")
        right_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        right_canvas = tk.Canvas(right_frame, bg="#E5ECEE", highlightthickness=0)
        right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
        right_scrollbar.pack(side=tk.RIGHT, fill="y")
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        self.right_inner_frame = tk.Frame(right_canvas, bg="#E5ECEE")
        right_canvas.create_window((0, 0), window=self.right_inner_frame, anchor="nw")
        self.right_inner_frame.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))
        right_canvas.pack(side=tk.LEFT, fill="both", expand=True)

        # Tiêu đề và nhãn chú thích
        tk.Label(self.right_inner_frame, text="Quá trình giải", font=("Arial", 10, "bold"), fg="#2C3E50", bg="#E5ECEE").pack(pady=5)
        self.note_label = tk.Label(self.right_inner_frame, text="Chọn môi trường và thuật toán để bắt đầu", font=("Arial", 8, "italic"), fg="#34495E", bg="#E5ECEE", wraplength=500)
        self.note_label.pack(pady=2)

        self.steps_frame = tk.Frame(self.right_inner_frame, bg="#E5ECEE")
        self.steps_frame.pack(fill="x", pady=5)
        self.steps_canvas = tk.Canvas(self.steps_frame, bg="#E5ECEE", height=360, width=600, scrollregion=(0, 0, 1200, 360))
        self.h_scrollbar = ttk.Scrollbar(self.steps_frame, orient="horizontal", command=self.steps_canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill="x")
        self.v_scrollbar_steps = ttk.Scrollbar(self.steps_frame, orient="vertical", command=self.steps_canvas.yview)
        self.v_scrollbar_steps.pack(side=tk.RIGHT, fill="y")
        self.steps_canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar_steps.set)
        self.inner_frame = tk.Frame(self.steps_canvas, bg="#E5ECEE")
        self.steps_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all")))
        self.steps_canvas.pack(side=tk.TOP, fill="x")

        self.pagination_frame = tk.Frame(self.right_inner_frame, bg="#E5ECEE")
        self.pagination_frame.pack(pady=5)
        self.prev_button = tk.Button(self.pagination_frame, text="Trước", command=self.prev_page, font=("Arial", 8), bg="#5DADE2", fg="white", padx=5, pady=2)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.page_label = tk.Label(self.pagination_frame, text="Trang 1", font=("Arial", 8), fg="#2C3E50", bg="#E5ECEE")
        self.page_label.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(self.pagination_frame, text="Sau", command=self.next_page, font=("Arial", 8), bg="#5DADE2", fg="white", padx=5, pady=2)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.info_frame = tk.Frame(self.right_inner_frame, bg="#E5ECEE")
        self.info_frame.pack(fill="x", pady=5)
        self.time_label = tk.Label(self.info_frame, text="Thời gian: Chưa có", font=("Arial", 8), fg="#2C3E50", bg="#E5ECEE")
        self.time_label.pack(anchor="w", padx=10, pady=5)
        self.steps_label = tk.Label(self.info_frame, text="Các bước: Chưa có", font=("Arial", 8), fg="#2C3E50", bg="#E5ECEE", wraplength=500, justify="left")
        self.steps_label.pack(anchor="w", padx=10, pady=5)

        # Nút điều khiển và chọn thuật toán
        control_frame = tk.Frame(self.root, bg="#2C3E50")
        control_frame.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

        # Chọn thuật toán
        algorithm_frame = tk.Frame(control_frame, bg="#2C3E50")
        algorithm_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(algorithm_frame, text="Chọn thuật toán:", font=("Arial", 10, "bold"), fg="white", bg="#2C3E50").pack(side=tk.LEFT, padx=5)
        methods = ["BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "IDA*", "Hill Climbing", "Steepest Ascent", 
                   "Stochastic Hill", "Simulated Annealing", "Beam Search", "AND - OR Search", "Genetic", 
                    "Backtracking", "Backtracking with Forward Checking", "Q_Learning"]
        method_combo = ttk.Combobox(algorithm_frame, textvariable=self.method, values=methods, font=("Arial", 10), state="readonly", width=20)
        method_combo.set("BFS")
        method_combo.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(control_frame, bg="#2C3E50")
        button_frame.pack(side=tk.RIGHT, padx=10)
        self.solve_button = tk.Button(button_frame, text="Solve", command=self.solve, font=("Arial", 10, "bold"), bg="#27AE60", fg="white", width=8, height=2)
        self.solve_button.pack(side=tk.LEFT, padx=5)
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset, font=("Arial", 10, "bold"), bg="#E74C3C", fg="white", width=8, height=2)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.status_frame = tk.Frame(self.root, bg="#2C3E50")
        self.status_frame.pack(side=tk.BOTTOM, fill="x", pady=5)
        self.status_label = tk.Label(self.status_frame, text="Đang chờ...", font=("Arial", 10, "bold"), fg="white", bg="#2C3E50")
        self.status_label.pack(side=tk.LEFT, padx=10)

    def update_environment(self):
        self.initial_belief_state = self.generate_initial_belief()
        self.current_belief_state = [state[:] for state in self.initial_belief_state]
        self.steps = []
        self.current_page = 0
        self.update_belief_display()
        print(f"Đã chuyển sang môi trường: {self.environment.get()}")

    def update_debug_display(self, message):
        print(message)

    def draw_state(self, canvas, state, x_offset=0, y_offset=0, size=30):
        canvas.delete("all")
        for i in range(3):
            for j in range(3):
                num = state[i][j]
                x0, y0 = j * size + x_offset, i * size + y_offset
                x1, y1 = x0 + size, y0 + size
                canvas.create_rectangle(x0, y0, x1, y1, fill="#5DADE2" if num != 0 else "#D5DBDB", outline="#2C3E50", width=1)
                if num != 0:
                    canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(num), font=("Arial", 12, "bold"), fill="white")

    def draw_initial_belief(self):
        for widget in self.initial_belief_inner.winfo_children():
            widget.destroy()
        
        for idx, state in enumerate(self.initial_belief_state):
            frame = tk.Frame(self.initial_belief_inner, bg="#E5ECEE", padx=5)
            frame.pack(pady=5)
            canvas = tk.Canvas(frame, width=120, height=100, bg="#E5ECEE", highlightthickness=0)
            canvas.pack()
            self.draw_state(canvas, state, x_offset=15, y_offset=10, size=30)
            tk.Label(frame, text=f"Trạng thái {idx + 1}", font=("Arial", 8), fg="#2C3E50", bg="#E5ECEE").pack()

    def draw_goal_state(self):
        self.goal_canvas.delete("all")
        self.draw_state(self.goal_canvas, goal_state, x_offset=15, y_offset=15, size=30)
        self.root.update()

    def update_belief_display(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Luôn vẽ lại niềm tin ban đầu bên khung trái
        self.draw_initial_belief()

        belief_states = [self.initial_belief_state]

        for step_action in self.steps:
            new_belief = []
            step_info = []
            for idx, (state, action_info) in enumerate(zip(belief_states[-1], step_action)):
                state_list = [list(row) for row in state]
                move, (blank_x, blank_y), (new_x, new_y) = action_info
                valid_actions = self.get_valid_actions(state_list)
                message = f"Step {len(belief_states)}, State {idx + 1}: {state_list}, Move: {move}, Valid actions: {valid_actions}"
                self.update_debug_display(message)

                if move != "NONE" and move in valid_actions:
                    new_state = self.apply_action(state_list, move, blank_x, blank_y, new_x, new_y)
                    new_belief.append(new_state)
                    step_info.append(f"Trạng thái {idx + 1}: {move} ({blank_x},{blank_y}) -> ({new_x},{new_y})")
                else:
                    message = f"Move {move} invalid or NONE for state {idx + 1}"
                    self.update_debug_display(message)
                    new_belief.append(state_list)
                    step_info.append(f"Trạng thái {idx + 1}: NONE")
            belief_states.append(new_belief)

        start_idx = self.current_page * self.states_per_page
        end_idx = min(start_idx + self.states_per_page, len(belief_states))
        states_to_display = belief_states[start_idx:end_idx]

        for i, belief in enumerate(states_to_display):
            step_frame = tk.Frame(self.inner_frame, bg="#E5ECEE", padx=10)
            step_frame.grid(row=0, column=i, padx=10, pady=5, sticky="n")

            step_number = start_idx + i
            step_text = "Niềm tin ban đầu" if step_number == 0 else f"Bước {step_number}"
            tk.Label(step_frame, text=step_text, font=("Arial", 8, "bold"), fg="#2C3E50", bg="#E5ECEE").pack(pady=2)

            for idx, state in enumerate(belief):
                state_frame = tk.Frame(step_frame, bg="#E5ECEE")
                state_frame.pack(pady=5)
                canvas = tk.Canvas(state_frame, width=120, height=100, bg="#E5ECEE", highlightthickness=0)
                canvas.pack()
                self.draw_state(canvas, state, x_offset=15, y_offset=10, size=30)
                tk.Label(state_frame, text=f"Trạng thái {idx + 1}", font=("Arial", 8), fg="#2C3E50", bg="#E5ECEE").pack()

        total_pages = (len(belief_states) + self.states_per_page - 1) // self.states_per_page
        self.page_label.config(text=f"Trang {self.current_page + 1}/{total_pages}")
        self.prev_button.config(state="normal" if self.current_page > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_page < total_pages - 1 else "disabled")
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_belief_display()

    def next_page(self):
        total_pages = (len(self.steps) + 1 + self.states_per_page - 1) // self.states_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_belief_display()

    def get_valid_actions(self, state):
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

    def apply_action(self, state, action, x, y, new_x, new_y):
        new_state = [row[:] for row in state]
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
        return new_state

    def solve(self):
        # Hiển thị chú thích trên giao diện và console
        env_name = "Partially Observable" if self.environment.get() == "partially_observable" else "Sensorless"
        note_text = f"Đang giải bằng {self.method.get()} trong môi trường {env_name}"
        self.note_label.config(text=note_text)
        print(note_text + "...")
        
        self.status_label.config(text="Đang giải...", fg="yellow")
        self.time_label.config(text="Thời gian: ...")
        self.steps_label.config(text="Các bước: Đang tính toán...")
        self.root.update()

        start_time = time.time()
        self.steps = []
        current_belief = [state[:] for state in self.initial_belief_state]

        # Áp dụng thuật toán trên trạng thái đầu tiên để lấy danh sách các bước đến đích
        solver = PuzzleSolver(current_belief[0], self.method.get())
        state_steps = solver.solve()
        print(f"Solver steps for reference state: {state_steps}")

        # Nếu không tìm thấy giải pháp cho trạng thái đầu tiên, dừng lại
        if not state_steps:
            self.time_label.config(text="Thời gian: 0 giây")
            self.steps_label.config(text="Các bước: Không tìm thấy giải pháp")
            self.status_label.config(text="Không tìm thấy đích!", fg="red")
            messagebox.showwarning("Thông báo", "Không tìm thấy giải pháp cho trạng thái tham chiếu!")
            return

        # Áp dụng các bước cho tất cả trạng thái trong belief state, đảm bảo đến đích
        self.current_belief_state = [state[:] for state in self.initial_belief_state]
        for move, (ref_x, ref_y), (new_x, new_y) in state_steps:
            step_action = []
            for state in self.current_belief_state:
                state_list = [list(row) for row in state]
                blank_x, blank_y = find_blank(state_list)  # Tìm vị trí ô trống trong trạng thái hiện tại
                
                # Điều chỉnh tọa độ di chuyển dựa trên ô trống
                valid = False
                if move == "UP" and blank_x - 1 >= 0 and (blank_x - 1, blank_y) == (new_x, new_y):
                    valid = True
                elif move == "DOWN" and blank_x + 1 < 3 and (blank_x + 1, blank_y) == (new_x, new_y):
                    valid = True
                elif move == "LEFT" and blank_y - 1 >= 0 and (blank_x, blank_y - 1) == (new_x, new_y):
                    valid = True
                elif move == "RIGHT" and blank_y + 1 < 3 and (blank_x, blank_y + 1) == (new_x, new_y):
                    valid = True
                
                if valid:
                    new_state = self.apply_action(state_list, move, blank_x, blank_y, new_x, new_y)
                    step_action.append((move, (blank_x, blank_y), (new_x, new_y)))
                else:
                    step_action.append(("NONE", (blank_x, blank_y), (blank_x, blank_y)))
            
            self.steps.append(step_action)
            # Áp dụng ngay để kiểm tra tiến trình
            new_belief = []
            for idx, (state, action_info) in enumerate(zip(self.current_belief_state, step_action)):
                state_list = [list(row) for row in state]
                move, (blank_x, blank_y), (new_x, new_y) = action_info
                if move != "NONE":
                    new_state = self.apply_action(state_list, move, blank_x, blank_y, new_x, new_y)
                    new_belief.append(new_state)
                else:
                    new_belief.append(state_list)
            self.current_belief_state = new_belief

            # Kiểm tra điều kiện dừng sau mỗi bước
            if self.environment.get() == "partially_observable":
                if any(state == goal_state for state in self.current_belief_state):
                    print("Stopping: At least one state reached the goal in Partially Observable environment.")
                    break
            elif self.environment.get() == "sensorless":
                if any(state == goal_state for state in self.current_belief_state):
                    print("Stopping: At least one state reached the goal in Sensorless environment.")
                    break


        end_time = time.time()
        total_time = round(end_time - start_time, 5)

        # Cập nhật giao diện ngay lập tức
        self.current_page = 0
        self.update_belief_display()

        step_descriptions = ["; ".join([f"Trạng thái {idx + 1}: {move} ({blank_x},{blank_y}) -> ({new_x},{new_y})" if move != "NONE" else f"Trạng thái {idx + 1}: NONE" for idx, (move, (blank_x, blank_y), (new_x, new_y)) in enumerate(step)]) for step in self.steps]
        self.time_label.config(text=f"Thời gian: {total_time} giây")
        steps_text = "Các bước: " + "; ".join(step_descriptions) if step_descriptions else "Các bước: Không tìm thấy giải pháp"
        self.steps_label.config(text=steps_text)

        if self.environment.get() == "partially_observable":
            # POS: Dừng khi bất kỳ trạng thái nào đạt đích
            if any(state == goal_state for state in self.current_belief_state):
                self.status_label.config(text="Đã hoàn thành!", fg="green")
                messagebox.showinfo("Thông báo", "Đã hoàn thành! Có ít nhất một trạng thái đạt đích.")
            else:
                self.status_label.config(text="Không tìm thấy đích!", fg="red")
                messagebox.showwarning("Thông báo", "Không tìm thấy trạng thái đích trong tập niềm tin sau nhiều bước!")
        else:
            # Sensorless: Dừng khi tất cả trạng thái đều đạt đích
            if any(state == goal_state for state in self.current_belief_state):
                self.status_label.config(text="Đã hoàn thành!", fg="green")
                messagebox.showinfo("Thông báo", "Đã hoàn thành! Có ít nhất một trạng thái đạt đích.")
            else:
                self.status_label.config(text="Không tìm thấy đích!", fg="red")
                messagebox.showwarning("Thông báo", "Không phải tất cả trạng thái đều đạt đích!")

    def reset(self):
        self.initial_belief_state = self.generate_initial_belief()
        self.current_belief_state = [state[:] for state in self.initial_belief_state]
        self.steps = []
        self.current_page = 0
        self.update_belief_display()
        self.note_label.config(text="Chọn môi trường và thuật toán để bắt đầu")
        self.status_label.config(text="Đang chờ...", fg="white")
        self.time_label.config(text="Thời gian: 0 giây")
        self.steps_label.config(text="Các bước: Chưa có")
        print("Đã reset giao diện.")