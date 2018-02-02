import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, app):
        super().__init__(app, relief=tk.RIDGE, bg='black', borderwidth=5)
        self.app = app


        f1 = tk.Frame(self, bg='black')
        f1.pack(fill=tk.X, side=tk.TOP)

        self.level_lbl = tk.Label(f1, text='level 1', bg='black', fg='white')
        self.level_lbl.pack()

        tk.Label(f1, text='score:', bg='black', fg='white').pack()
        self.score_lbl = tk.Label(f1, bg='black', fg='white', width=10,
                                  borderwidth=3, relief=tk.RIDGE)
        self.score_lbl.pack()

        tk.Label(f1, text='lines cleared:', bg='black', fg='white').pack()
        self.row_count_lbl = tk.Label(f1, bg='black', fg='white', width=10,
                                      borderwidth=3, relief=tk.RIDGE)
        self.row_count_lbl.pack()


        f2 = tk.Frame(self, bg='black')
        f2.pack(fill=tk.X, expand=True)
        tk.Label(f2, text='next brick:', bg='black', fg='white').pack()
        self.nbl = tk.Label(f2, text='aaa')
        self.nbl.pack()

    def update_next_brick(self, name, *__):
        next_brick = self.app.globalgetvar(name)
        self.nbl['text'] = next_brick

    def update_rows_count(self, name, *__):
        rows_cleared = self.app.globalgetvar(name)
        self.row_count_lbl['text'] = rows_cleared

    def update_score(self, name, *__):
        score = self.app.globalgetvar(name)
        self.score_lbl['text'] = score

    def update_level(self, level):
        self.level_lbl['text'] = f'level {level}'


