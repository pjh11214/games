import tkinter as tk
import random


class MineSweeper:
    def __init__(self, root, rows=10, cols=10, bomb_count=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.bomb_count = bomb_count
        self.buttons = []  # 初始化一个空的按钮列表

        self.root.title("扫雷游戏")
        self.root.configure(bg="#f0f0f0")
        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        # 创建游戏标题和说明
        self.title_label = tk.Label(self.root, text="扫雷游戏", font=("Arial", 24), bg="#f0f0f0")
        self.title_label.grid(row=0, columnspan=self.cols, padx=10, pady=10)

        self.instructions_label = tk.Label(self.root, text="右键点击标记炸弹，成功打开所有安全格子赢得游戏！",
                                           bg="#f0f0f0")
        self.instructions_label.grid(row=1, columnspan=self.cols)

        # 控制面板
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.grid(row=self.rows-10, columnspan=self.cols, pady=(10, 10))

        # 创建重新开始按钮
        self.restart_button = tk.Button(control_frame, text="重新开始", command=self.restart_game, font=("Arial", 12),
                                        bg="#d1e7dd", fg="#0f5132")
        self.restart_button.grid(row=0, column=0, padx=10)

        self.timer_label = tk.Label(control_frame, text="时间: 0", font=("Arial", 12), bg="#f0f0f0")
        self.timer_label.grid(row=0, column=1)

        self.difficulty_label = tk.Label(control_frame, text="选择难度:", font=("Arial", 12), bg="#f0f0f0")
        self.difficulty_label.grid(row=0, column=2)

        self.difficulty_var = tk.StringVar(value='easy')

        self.easy_button = tk.Radiobutton(control_frame, text="简单", variable=self.difficulty_var, value='easy',
                                          command=self.set_difficulty, bg="#f0f0f0", indicatoron=False)
        self.medium_button = tk.Radiobutton(control_frame, text="中等", variable=self.difficulty_var, value='medium',
                                            command=self.set_difficulty, bg="#f0f0f0", indicatoron=False)
        self.hard_button = tk.Radiobutton(control_frame, text="困难", variable=self.difficulty_var, value='hard',
                                          command=self.set_difficulty, bg="#f0f0f0", indicatoron=False)

        self.easy_button.grid(row=0, column=3, padx=5)
        self.medium_button.grid(row=0, column=4, padx=5)
        self.hard_button.grid(row=0, column=5, padx=5)

        # 自定义棋盘大小和雷数量输入
        self.custom_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.custom_frame.grid(row=self.rows + 3, columnspan=self.cols, pady=(10, 0))

        self.rows_label = tk.Label(self.custom_frame, text="行数:", bg="#f0f0f0")
        self.rows_label.grid(row=0, column=0)

        self.rows_entry = tk.Entry(self.custom_frame, width=5)
        self.rows_entry.insert(0, str(self.rows))
        self.rows_entry.grid(row=0, column=1)

        self.cols_label = tk.Label(self.custom_frame, text="列数:", bg="#f0f0f0")
        self.cols_label.grid(row=0, column=2)

        self.cols_entry = tk.Entry(self.custom_frame, width=5)
        self.cols_entry.insert(0, str(self.cols))
        self.cols_entry.grid(row=0, column=3)

        self.bombs_label = tk.Label(self.custom_frame, text="雷的数量:", bg="#f0f0f0")
        self.bombs_label.grid(row=0, column=4)

        self.bombs_entry = tk.Entry(self.custom_frame, width=5)
        self.bombs_entry.insert(0, str(self.bomb_count))
        self.bombs_entry.grid(row=0, column=5)

        self.set_custom_button = tk.Button(self.custom_frame, text="设置", command=self.set_custom_parameters)
        self.set_custom_button.grid(row=0, column=6)

    def initialize_game(self):
        # 初始化按钮列表
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # 销毁现有按钮
        for r in range(self.rows):
            for c in range(self.cols):
                if self.buttons[r][c] is not None:
                    self.buttons[r][c].destroy()

        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_board()
        self.create_buttons()
        self.game_over = False
        self.first_click = True
        self.elapsed_time = 0
        self.timer_label.config(text="时间: 0")  # 重置计时器显示
        self.root.after(1000, self.update_timer)

    def create_board(self):
        bombs_placed = 0
        while bombs_placed < self.bomb_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] == 0:
                self.board[r][c] = 'B'
                bombs_placed += 1

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 'B':
                    self.board[r][c] = self.count_bombs(r, c)

    def count_bombs(self, r, c):
        bomb_count = 0
        for i in range(max(0, r - 1), min(self.rows, r + 2)):
            for j in range(max(0, c - 1), min(self.cols, c + 2)):
                if self.board[i][j] == 'B':
                    bomb_count += 1
        return bomb_count

    def create_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, text='', font=("Arial", 14), width=2, height=1, bg="#e0e0e0",
                                command=lambda r=r, c=c: self.reveal(r, c), relief="raised")
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.toggle_flag(r, c))  # 右键标记炸弹
                btn.grid(row=r + 2, column=c, padx=1, pady=1)  # 适当间距
                self.buttons[r][c] = btn  # 将按钮存储在 buttons 列表中

    def reveal(self, r, c):
        if self.game_over:
            return

        if self.first_click:
            self.first_click = False
            self.start_time = self.root.after(1000, self.update_timer)

        if self.board[r][c] == 'B':
            self.buttons[r][c]['text'] = '💣'
            self.buttons[r][c].config(bg="#ffdddd", relief="sunken")
            self.game_over = True
            self.show_all_bombs()
            self.timer_label.config(text="游戏结束!", fg="red")
            if self.start_time is not None:
                self.root.after_cancel(self.start_time)

        else:
            self.buttons[r][c]['text'] = str(self.board[r][c]) if self.board[r][c] > 0 else ''
            self.buttons[r][c]['state'] = 'disabled'
            self.buttons[r][c].config(bg="#ffffff", relief="sunken")
            if self.board[r][c] == 0:
                self.reveal_neighbors(r, c)

        if self.check_win():
            self.game_over = True
            self.timer_label.config(text=f"你赢了! 用时: {self.elapsed_time} 秒", fg="green")
            if self.start_time is not None:
                self.root.after_cancel(self.start_time)

    def toggle_flag(self, r, c):
        if self.game_over:
            return
        current_text = self.buttons[r][c]['text']
        if current_text == '':
            self.buttons[r][c]['text'] = '🚩'
            self.buttons[r][c].config(bg="#ffeeba", relief="raised")
        elif current_text == '🚩':
            self.buttons[r][c]['text'] = ''
            self.buttons[r][c].config(bg="#e0e0e0", relief="raised")

    def reveal_neighbors(self, r, c):
        # 使用栈代替递归来避免深度递归的问题
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            for i in range(max(0, cr - 1), min(self.rows, cr + 2)):
                for j in range(max(0, cc - 1), min(self.cols, cc + 2)):
                    if self.buttons[i][j]['state'] == 'normal':
                        self.reveal(i, j)
                        if self.board[i][j] == 0:
                            stack.append((i, j))  # 如果是0，继续揭示邻居

    def show_all_bombs(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'B':
                    self.buttons[r][c]['text'] = '💣'
                    self.buttons[r][c].config(bg="#ffdddd")
                elif self.buttons[r][c]['text'] == '🚩':
                    self.buttons[r][c]['text'] = '🚩 (误标)'

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 'B' and self.buttons[r][c]['state'] == 'normal':
                    return False
        return True

    def update_timer(self):
        if not self.game_over:
            self.elapsed_time += 1
            self.timer_label.config(text=f"时间: {self.elapsed_time}")
            self.start_time = self.root.after(1000, self.update_timer)

    def restart_game(self):
        if self.start_time is not None:
            self.root.after_cancel(self.start_time)  # 取消之前的定时器
        self.initialize_game()

    def set_custom_parameters(self):
        try:
            custom_rows = int(self.rows_entry.get())
            custom_cols = int(self.cols_entry.get())
            custom_bombs = int(self.bombs_entry.get())

            if custom_rows < 1 or custom_cols < 1 or custom_bombs < 1:
                raise ValueError("行数、列数和雷的数量必须大于0")

            self.rows, self.cols, self.bomb_count = custom_rows, custom_cols, custom_bombs
            if self.bomb_count > self.rows * self.cols:
                raise ValueError("雷的数量不能大于格子的总数")

            self.restart_game()

        except ValueError as ve:
            print(f"输入错误: {ve}")

    def set_difficulty(self):
        difficulty = self.difficulty_var.get()
        if difficulty == 'easy':
            self.rows, self.cols, self.bomb_count = 8, 8, 10
        elif difficulty == 'medium':
            self.rows, self.cols, self.bomb_count = 16, 30, 99
        elif difficulty == 'hard':
            self.rows, self.cols, self.bomb_count = 20,35,150
        self.restart_game()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # 设置主窗口大小
    ms = MineSweeper(root)

    root.mainloop()
