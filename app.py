import tkinter as tk
from board import Board
from sidebar import Sidebar


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Tetris')
        self.resizable(False, False)
        self._load_images()

        self.level = 1
        self.score = tk.IntVar()
        self.line_count = tk.IntVar()
        self.next_brick_in_queue = tk.StringVar()

        self.sidebar = Sidebar(self)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        self.next_brick_in_queue.trace('w', self.sidebar.update_next_brick)

        self.line_count.trace('w', self.sidebar.update_rows_count)
        self.line_count.set(0)

        self.score.trace('w', self.sidebar.update_score)
        self.score.set(0)

        self.board = Board(self, self.images)
        self.board.pack(side=tk.LEFT)

    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            new_points = self.level * 40
        elif lines_cleared == 2:
            new_points = self.level * 100
        elif lines_cleared == 3:
            new_points = self.level * 300
        elif lines_cleared == 4:
            new_points = self.level * 1200
        else:
            raise ValueError

        new_score = self.score.get() + new_points
        self.score.set(new_score)

        old_lines_count = self.line_count.get()
        new_lines_count = old_lines_count + lines_cleared
        self.line_count.set(new_lines_count)

        if old_lines_count // 10 != new_lines_count // 10:
            self._level_up()

    def game_over(self):
        msg = f'\nGAME OVER\n\n' \
              f'Your score is {self.score.get()} points.\n' \
              f'Press spacebar to play again.\n'
        score_lbl = tk.Label(self.board, text=msg)
        score_lbl.place(anchor=tk.CENTER, relx=.5, rely=.5)
        self.bind('<space>', self.restart_game)

    def restart_game(self, *__):
        self.board.destroy()
        self.line_count.set(0)
        self.score.set(0)
        self.level = 1
        self.sidebar.update_level(self.level)
        self.board = Board(self, self.images)
        self.board.pack(side=tk.LEFT)

    def _level_up(self):
        self.level += 1
        self.sidebar.update_level(self.level)
        self.board.tick_time = int(self.board.tick_time * 0.9)

    def _load_images(self):
        self.images = {'green':     tk.PhotoImage(file='img/green.png'),
                       'red':       tk.PhotoImage(file='img/red.png'),
                       'blue':      tk.PhotoImage(file='img/blue.png'),
                       'cyan':      tk.PhotoImage(file='img/cyan.png'),
                       'magenta':   tk.PhotoImage(file='img/magenta.png'),
                       'orange':    tk.PhotoImage(file='img/orange.png'),
                       'yellow':    tk.PhotoImage(file='img/yellow.png'),
                       'black':     tk.PhotoImage(file='img/black.png'),
                       'grey':      tk.PhotoImage(file='img/grey.png')}
