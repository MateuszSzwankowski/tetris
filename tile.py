import tkinter as tk


class Tile(tk.Label):
    def __init__(self, board, row, column):
        self.row = row
        self.column = column
        self.has_brick = False

        if (row + column) % 2:
            self.default_color = 'black'
        else:
            self.default_color = 'grey'

        super().__init__(board, text=' ', width=20, height=20,
                         image=board.images[self.default_color],
                         compound=tk.CENTER)
        self.grid(row=row, column=column)
