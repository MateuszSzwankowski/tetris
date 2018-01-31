import tkinter as tk


class Menu(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=100, relief=tk.RIDGE, bg='black', borderwidth=5)
