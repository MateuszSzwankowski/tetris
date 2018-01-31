import tkinter as tk
import time

from tile import Tile
from brick import Brick


class Board(tk.Frame):
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22
    INITIAL_TICK_TIME = 1000

    def __init__(self, app, images):
        super().__init__(app, bg='black', width=200, height=200)

        self.images = images
        self.tick_time = Board.INITIAL_TICK_TIME
        self.app = app
        self.tiles = [[Tile(self, row, column)
                       for column in range(self.BOARD_WIDTH)]
                      for row in range(self.BOARD_HEIGHT)]

        # hide top 2 rows
        for row in self.tiles[0:2]:
            for t in row:
                t.grid_forget()

        self.bricks = set()
        self._spawn_brick()
        self.active = True

        app.bind('<Right>', self._handle_command)
        app.bind('<Left>', self._handle_command)
        app.bind('<Down>', self._handle_command)
        app.bind('<Up>', self._handle_command)
        app.bind('<space>', self._handle_command)

        self._tick()

    def _spawn_brick(self):
        self.brick = Brick(self)

    def spawn_next(self):
        self.bricks |= self.brick.tiles
        del self.brick
        self._spawn_brick()
        self._remove_full_rows()
        if self.is_collisions(self.brick.coords):
            self.active = False
            self.app.game_over()
            print('Game over')
        else:
            self.brick.move_down()

    def _handle_command(self, event):
        command = event.keysym
        if not self.active:
            return
        elif command == 'Right':
            self.brick.move_right()
        elif command == 'Left':
            self.brick.move_left()
        elif command == 'Up':
            self.brick.rotate()
        elif command == 'Down':
            self.brick.move_down()
        elif command == 'space':
            self._hard_drop()

    def _remove_full_rows(self):
        full_rows = []
        for i, row in enumerate(self.tiles):
            if (set(row) & self.bricks) == set(row):
                self.bricks -= set(row)
                full_rows.append(i)

        if not full_rows:
            return

        for line in sorted(full_rows):
            for row in range(line, 1, -1):
                for i, tile in enumerate(self.tiles[row]):
                    tile_above = self.tiles[row - 1][i]
                    if tile_above.has_brick:
                        tile_above.has_brick = False
                        tile.has_brick = True
                        tile['image'] = self.tiles[row - 1][i]['image']
                    else:
                        tile.has_brick = False
                        tile['image'] = self.images[tile.default_color]
            old_bricks = self.bricks.copy()
            self.bricks = {self.tiles[t.row + 1][t.column]
                           for t in old_bricks if t.row <= line}
            self.bricks |= {t for t in old_bricks if t.row > line}
            self.app.update()
            time.sleep(0.1)

    def _tick(self):
        if self.active:
            self.brick.move_down()
            self.app.after(self.tick_time, self._tick)

    def _hard_drop(self):
        self.brick.dropping = True
        while self.brick.dropping:
            self.brick.move_down()

    def is_collisions(self, new_coordinates):
        tiles = {self.tiles[r][c] for r, c in new_coordinates}
        return bool(self.bricks & tiles)
