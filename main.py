import tkinter as tk
from gui.puzzle_gui import PuzzleGUI
from gui.complex_environment_gui import ComplexEnvironmentGUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver Menu")
        self.root.geometry("300x250")
        self.root.configure(bg="#2C3E50")
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="8-Puzzle Solver", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50")
        title_label.pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=10)

        simple_gui_button = tk.Button(button_frame, text="Mở giao diện đơn giản", command=self.open_simple_gui, font=("Arial", 12), bg="#3498DB", fg="white", width=25)
        simple_gui_button.pack(pady=5)

        complex_gui_button = tk.Button(button_frame, text="Mở Giao diện Phức tạp", command=self.open_complex_gui, font=("Arial", 12), bg="#3498DB", fg="white", width=25)
        complex_gui_button.pack(pady=5)

        exit_button = tk.Button(button_frame, text="Thoát", command=self.root.quit, font=("Arial", 12), bg="#E74C3C", fg="white", width=15, height=2)
        exit_button.pack(pady=5)

    def open_simple_gui(self):
        new_window = tk.Toplevel(self.root)
        app = PuzzleGUI(new_window)

    def open_complex_gui(self):
        new_window = tk.Toplevel(self.root)
        app = ComplexEnvironmentGUI(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()