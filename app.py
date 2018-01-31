import tkinter as tk
from board import Board
from menu import Menu


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tetris')
        self.resizable(False, False)
        self._load_images()

        self.board = Board(self, self.images)
        self.board.pack(side=tk.LEFT)

        self.menu = Menu(self)
        self.menu.pack(side=tk.RIGHT, expand=True, fill=tk.Y)

    def restart_game(self):
        raise NotImplementedError

    def game_over(self):
        raise NotImplementedError

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
