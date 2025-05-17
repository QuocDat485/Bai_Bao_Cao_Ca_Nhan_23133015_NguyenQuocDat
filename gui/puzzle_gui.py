import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
from solvers.base_solver import PuzzleSolver
from utils.helpers import goal_state, find_blank, swap

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1400x800")
        self.root.configure(bg="#2C3E50")
        self.initial_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
        #self.initial_state = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        self.state = [row[:] for row in self.initial_state]
        self.method = tk.StringVar(value="BFS")
        self.steps = []
        self.current_page = 0
        self.states_per_page = 8
        self.create_widgets()
        self.update_grid()
        self.draw_goal_state()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="8-Puzzle Solver", font=("Arial", 20, "bold"), fg="white", bg="#2C3E50")
        title_label.pack(pady=10)

        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#2C3E50", width=200)
        left_frame.pack(side=tk.LEFT, fill="y", padx=10)

        tk.Label(left_frame, text="Trạng thái bắt đầu", font=("Arial", 12, "bold"), fg="white", bg="#2C3E50").pack(pady=5)
        self.start_canvas = tk.Canvas(left_frame, width=150, height=150, bg="#F39C12", highlightthickness=2, highlightbackground="#34495E")
        self.start_canvas.pack(pady=5)
        self.draw_start_state()

        tk.Label(left_frame, text="Trạng thái hiện tại", font=("Arial", 12, "bold"), fg="white", bg="#2C3E50").pack(pady=5)
        self.canvas = tk.Canvas(left_frame, width=150, height=150, bg="#ECF0F1", highlightthickness=2, highlightbackground="#34495E")
        self.canvas.pack(pady=5)

        tk.Label(left_frame, text="Trạng thái đích", font=("Arial", 12, "bold"), fg="white", bg="#2C3E50").pack(pady=5)
        self.goal_canvas = tk.Canvas(left_frame, width=150, height=150, bg="#2ECC71", highlightthickness=2, highlightbackground="#34495E")
        self.goal_canvas.pack(pady=5)

        right_frame = tk.Frame(main_frame, bg="#2C3E50")
        right_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        tk.Label(right_frame, text="Quá trình giải", font=("Arial", 12, "bold"), fg="white", bg="#2C3E50").pack(pady=5)
        self.steps_frame = tk.Frame(right_frame, bg="#ECF0F1")
        self.steps_frame.pack(fill="x", pady=5)
        self.steps_canvas = tk.Canvas(self.steps_frame, bg="#ECF0F1", height=180, width=1000, scrollregion=(0, 0, 2000, 180))
        self.h_scrollbar = ttk.Scrollbar(self.steps_frame, orient="horizontal", command=self.steps_canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill="x")
        self.steps_canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.steps_canvas.pack(side=tk.TOP, fill="x")
        self.inner_frame = tk.Frame(self.steps_canvas, bg="#ECF0F1")
        self.steps_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all")))

        self.pagination_frame = tk.Frame(right_frame, bg="#2C3E50")
        self.pagination_frame.pack(pady=5)
        self.prev_button = tk.Button(self.pagination_frame, text="Trước", command=self.prev_page, font=("Arial", 10), bg="#3498DB", fg="white")
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.page_label = tk.Label(self.pagination_frame, text="Trang 1", font=("Arial", 10), fg="white", bg="#2C3E50")
        self.page_label.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(self.pagination_frame, text="Sau", command=self.next_page, font=("Arial", 10), bg="#3498DB", fg="white")
        self.next_button.pack(side=tk.LEFT, padx=5)

        tk.Label(self.pagination_frame, text="Tìm trang:", font=("Arial", 10), fg="white", bg="#2C3E50").pack(side=tk.LEFT, padx=5)
        self.page_entry = tk.Entry(self.pagination_frame, width=5, font=("Arial", 10))
        self.page_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(self.pagination_frame, text="Tìm", command=self.search_page, font=("Arial", 10), bg="#3498DB", fg="white")
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.info_frame = tk.Frame(right_frame, bg="#2C3E50")
        self.info_frame.pack(fill="x", pady=5)
        self.time_label = tk.Label(self.info_frame, text="Thời gian: Chưa có", font=("Arial", 10), fg="white", bg="#2C3E50")
        self.time_label.pack(anchor="w", padx=10, pady=2)
        self.steps_label = tk.Label(self.info_frame, text="Các bước: Chưa có", font=("Arial", 10), fg="white", bg="#2C3E50", wraplength=900, justify="left")
        self.steps_label.pack(anchor="w", padx=10, pady=2)

        control_frame = tk.Frame(self.root, bg="#2C3E50")
        control_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(control_frame, text="Chọn phương pháp:", font=("Arial", 12, "bold"), fg="white", bg="#2C3E50").pack(side=tk.LEFT, padx=10)
        methods = ["BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "IDA*", "Hill Climbing", "Steepest Ascent", 
                   "Stochastic Hill", "Simulated Annealing", "Beam Search", "AND - OR Search", "Genetic" 
                   , "Backtracking", "Backtracking with Forward Checking", "Q_Learning" ]
        method_combo = ttk.Combobox(control_frame, textvariable=self.method, values=methods, font=("Arial", 10), state="readonly", width=20)
        method_combo.set("BFS")
        method_combo.pack(side=tk.LEFT, padx=10)

        button_frame = tk.Frame(control_frame, bg="#2C3E50")
        button_frame.pack(side=tk.RIGHT, padx=10)
        self.solve_button = tk.Button(button_frame, text="Solve", command=self.solve, font=("Arial", 12, "bold"), bg="#27AE60", fg="white", width=8, height=1)
        self.solve_button.pack(side=tk.LEFT, padx=10)
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset, font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", width=8, height=1)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.status_frame = tk.Frame(self.root, bg="#2C3E50")
        self.status_frame.pack(fill="x", pady=10)
        self.status_label = tk.Label(self.status_frame, text="Đang chờ...", font=("Arial", 12, "bold"), fg="white", bg="#2C3E50")
        self.status_label.pack(side=tk.LEFT, padx=10)

    def update_grid(self):
        self.canvas.delete("all")
        for i in range(3):
            for j in range(3):
                num = self.state[i][j]
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#3498DB" if num != 0 else "#ECF0F1", outline="#2C3E50", width=2)
                if num != 0:
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(num), font=("Arial", 16, "bold"), fill="white")
        self.root.update()

    def draw_goal_state(self):
        self.goal_canvas.delete("all")
        for i in range(3):
            for j in range(3):
                num = goal_state[i][j]
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.goal_canvas.create_rectangle(x0, y0, x1, y1, fill="#2ECC71" if num != 0 else "#ECF0F1", outline="#2C3E50", width=2)
                if num != 0:
                    self.goal_canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(num), font=("Arial", 16, "bold"), fill="white")
        self.root.update()

    def draw_start_state(self):
        self.start_canvas.delete("all")
        for i in range(3):
            for j in range(3):
                num = self.state[i][j]
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.start_canvas.create_rectangle(x0, y0, x1, y1, fill="#F39C12" if num != 0 else "#ECF0F1", outline="#2C3E50", width=2)
                if num != 0:
                    self.start_canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(num), font=("Arial", 16, "bold"), fill="white")
        self.root.update()

    def draw_state(self, canvas, state, step_num):
        canvas.delete("all")
        for i in range(3):
            for j in range(3):
                num = state[i][j]
                x0, y0 = j * 40, i * 40
                x1, y1 = x0 + 40, y0 + 40
                canvas.create_rectangle(x0, y0, x1, y1, fill="#3498DB" if num != 0 else "#ECF0F1", outline="#2C3E50", width=2)
                if num != 0:
                    canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(num), font=("Arial", 12, "bold"), fill="white")
        canvas.create_text(60, 130, text=f"Bước {step_num}", font=("Arial", 10, "bold"), fill="black")
        from utils.helpers import heuristic
        canvas.create_text(60, 150, text=f"Manhattan: {heuristic(state)}", font=("Arial", 8), fill="black")

    def update_steps_display(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        states = [[row[:] for row in self.initial_state]]
        current_state = [row[:] for row in self.initial_state]

        for move, (x, y), (new_x, new_y) in self.steps:
            current_state = swap(current_state, x, y, new_x, new_y)
            states.append([row[:] for row in current_state])

        start_idx = self.current_page * self.states_per_page
        end_idx = min(start_idx + self.states_per_page, len(states))
        states_to_display = states[start_idx:end_idx]

        for i, state in enumerate(states_to_display):
            canvas = tk.Canvas(self.inner_frame, width=120, height=160, bg="#ECF0F1")
            canvas.grid(row=0, column=i, padx=5, pady=5)
            self.draw_state(canvas, state, start_idx + i)

        total_pages = (len(states) + self.states_per_page - 1) // self.states_per_page
        self.page_label.config(text=f"Trang {self.current_page + 1}/{total_pages}")
        self.prev_button.config(state="normal" if self.current_page > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_page < total_pages - 1 else "disabled")
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_steps_display()

    def next_page(self):
        total_pages = (len(self.steps) + 1 + self.states_per_page - 1) // self.states_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_steps_display()

    def search_page(self):
        try:
            page_num = int(self.page_entry.get()) - 1
            total_pages = (len(self.steps) + 1 + self.states_per_page - 1) // self.states_per_page
            if 0 <= page_num < total_pages:
                self.current_page = page_num
                self.update_steps_display()
            else:
                messagebox.showwarning("Lỗi", f"Vui lòng nhập số trang từ 1 đến {total_pages}")
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập một số hợp lệ")

    def solve(self):
        self.status_label.config(text="Đang giải...", fg="yellow")
        self.time_label.config(text="Thời gian: ...")
        self.steps_label.config(text="Các bước: Đang tính toán...")
        self.root.update()

        start_time = time.time()
        solver = PuzzleSolver(self.initial_state, self.method.get())

        if self.method.get() == "Sensorless Belief State Search":
            print("Belief State ban đầu:")
            belief_state = set()
            belief_state.add(tuple(map(tuple, self.initial_state)))
            temp_state = [row[:] for row in self.initial_state]
            for _ in range(2):
                x, y = find_blank(temp_state)
                directions = [(0, 1, "RIGHT"), (1, 0, "DOWN"), (0, -1, "LEFT"), (-1, 0, "UP")]
                random.shuffle(directions)
                for dx, dy, _ in directions:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < 3 and 0 <= new_y < 3:
                        temp_state = swap(temp_state, x, y, new_x, new_y)
                        belief_state.add(tuple(map(tuple, temp_state)))
                        break
            for state in belief_state:
                state_list = [list(row) for row in state]
                print(state_list)

        self.steps = solver.solve()
        end_time = time.time()
        total_time = round(end_time - start_time, 5)

        self.current_page = 0
        self.update_steps_display()

        current_state = [row[:] for row in self.initial_state]
        for move, (x, y), (new_x, new_y) in self.steps:
            current_state = swap(current_state, x, y, new_x, new_y)
            self.state = [row[:] for row in current_state]
            self.update_grid()
            time.sleep(0.5)

        self.time_label.config(text=f"Thời gian: {total_time} giây")
        steps_text = "Các bước: " + ", ".join([f"{move} ({x},{y}) -> ({new_x},{new_y})" for move, (x, y), (new_x, new_y) in self.steps])
        self.steps_label.config(text=steps_text)

        if self.state == goal_state:
            self.status_label.config(text="Đã hoàn thành!", fg="green")
            messagebox.showinfo("Thông báo", "Đã hoàn thành! Puzzle đã được giải thành công.")
        else:
            self.status_label.config(text="Không tìm được đường đi!", fg="red")
            messagebox.showwarning("Thông báo", "Không tìm được đường đi đến trạng thái đích!")

    def move_blank(self, x, y):
        blank_x, blank_y = find_blank(self.state)
        self.state = swap(self.state, blank_x, blank_y, x, y)
        self.update_grid()

    def reset(self):
        self.state = [row[:] for row in self.initial_state]
        self.steps = []
        self.current_page = 0
        self.update_grid()
        self.update_steps_display()
        self.status_label.config(text="Đang chờ...", fg="white")
        self.time_label.config(text="Thời gian: 0 giây")
        self.steps_label.config(text="Các bước: Chưa có")
