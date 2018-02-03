import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, app):
        self.app = app
        self._load_images()

        super().__init__(app, relief=tk.RIDGE, bg='black', borderwidth=5)

        self.level_lbl = tk.Label(self, text='LEVEL 1', bg='black', fg='white')
        self.level_lbl.pack()
        tk.Label(self, bg='black').pack(fill=tk.X)

        self.score_lbl = tk.Label(self, bg='black', fg='white', width=9,
                                  borderwidth=3, relief=tk.SUNKEN)
        tk.Label(self, text='SCORE:', bg='black', fg='white').pack()
        self.score_lbl.pack()

        tk.Label(self, text='LINES:', bg='black', fg='white').pack()
        self.row_count_lbl = tk.Label(self, bg='black', fg='white', width=9,
                                      borderwidth=3, relief=tk.SUNKEN)
        self.row_count_lbl.pack()

        tk.Label(self, bg='black').pack(fill=tk.X)
        tk.Label(self, bg='black').pack(fill=tk.X)

        tk.Label(self, text='NEXT:', bg='black', fg='white').pack()

        self.next_brick_label = tk.Label(self, text='', bg='black', width=75, height=50,
                                         borderwidth=3, relief=tk.SUNKEN)
        self.next_brick_label.pack()

        # buttons_frame = tk.Frame(self, bg='black')
        # buttons_frame.pack(fill=tk.X, side=tk.BOTTOM)
        #
        # self.new_game_btn = tk.Button(buttons_frame, text='new game')
        # self.new_game_btn.pack(fill=tk.X)
        #
        # self.pause_btn = tk.Button(buttons_frame, text='pause')
        # self.pause_btn.pack(fill=tk.X)
        #
        # self.high_scores_btn = tk.Button(buttons_frame, text='best scores')
        # self.high_scores_btn.pack(fill=tk.X)

    def update_rows_count(self, name, *__):
        rows_cleared = self.app.globalgetvar(name)
        self.row_count_lbl['text'] = rows_cleared

    def update_score(self, name, *__):
        score = self.app.globalgetvar(name)
        self.score_lbl['text'] = score

    def update_level(self, level):
        self.level_lbl['text'] = f'LEVEL {level}'

    def update_next_brick(self, name, *__):
        next_brick = self.app.globalgetvar(name)
        self.next_brick_label['image'] = self.brick_images[next_brick]

    def _load_images(self):
        self.brick_images = {'I': tk.PhotoImage(file='img/I.png'),
                             'O': tk.PhotoImage(file='img/O.png'),
                             'T': tk.PhotoImage(file='img/T.png'),
                             'S': tk.PhotoImage(file='img/S.png'),
                             'Z': tk.PhotoImage(file='img/Z.png'),
                             'J': tk.PhotoImage(file='img/J.png'),
                             'L': tk.PhotoImage(file='img/L.png')}

