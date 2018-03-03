import tkinter as tk
import numpy as np
import random

from .tile import Tile
from .brick import Brick


class Board(tk.Frame):
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22
    INITIAL_TICK_TIME = 800

    # first point is a pivot used in brick rotation
    BRICK_TYPES = [{'type': 'I', 'color': 'cyan',    'init_pos': np.array([[1, 5], [1, 3], [1, 4], [1, 6]])},
                   {'type': 'O', 'color': 'yellow',  'init_pos': np.array([[1, 4], [1, 5], [0, 4], [0, 5]])},
                   {'type': 'T', 'color': 'magenta', 'init_pos': np.array([[0, 4], [0, 3], [0, 5], [1, 4]])},
                   {'type': 'S', 'color': 'green',   'init_pos': np.array([[1, 4], [0, 4], [0, 5], [1, 3]])},
                   {'type': 'Z', 'color': 'red',     'init_pos': np.array([[1, 4], [0, 3], [0, 4], [1, 5]])},
                   {'type': 'J', 'color': 'blue',    'init_pos': np.array([[1, 4], [0, 3], [1, 5], [1, 3]])},
                   {'type': 'L', 'color': 'orange',  'init_pos': np.array([[1, 4], [0, 5], [1, 3], [1, 5]])}]

    def __init__(self, app, images):
        super().__init__(app, bg='black', width=200, height=200)

        self.images = images
        self.tick_time = Board.INITIAL_TICK_TIME
        self.app = app
        self._rows_cleared = 0
        self.tiles = [[Tile(self, row, column)
                       for column in range(self.BOARD_WIDTH)]
                      for row in range(self.BOARD_HEIGHT)]

        # hide top 2 rows
        for row in self.tiles[0:2]:
            for t in row:
                t.grid_forget()

        self.bricks = set()
        self._fill_brick_queue()
        active_brick_type = self.brick_queue.pop()
        self.active_brick = Brick(self, active_brick_type)
        self.app.next_brick_in_queue.set(self.brick_queue[-1]['type'])

        self.active = True

        app.bind('<Right>', self._handle_command)
        app.bind('<Left>',  self._handle_command)
        app.bind('<Down>',  self._handle_command)
        app.bind('<Up>',    self._handle_command)
        app.bind('<space>', self._handle_command)

        self._tick()

    def spawn_next_brick(self):
        self.bricks |= self.active_brick.tiles
        del self.active_brick
        self.active_brick = Brick(self, self.brick_queue.pop())

        if not self.brick_queue:
            self._fill_brick_queue()

        next_brick = self.brick_queue[-1]
        self.app.next_brick_in_queue.set(next_brick['type'])

        full_lines = self._find_full_lines()
        if full_lines:
            self.app.update_score(lines_cleared=len(full_lines))
            self._remove_full_lines(full_lines)

        if self.is_collision(self.active_brick.coords):
            self.active = False
            self.app.game_over()
        else:
            self.active_brick.move_down()

    def _fill_brick_queue(self):
        self.brick_queue = random.sample(Board.BRICK_TYPES,
                                         len(Board.BRICK_TYPES))

    def _handle_command(self, event):
        command = event.keysym
        if not self.active:
            return
        elif command == 'Right':
            self.active_brick.move_right()
        elif command == 'Left':
            self.active_brick.move_left()
        elif command == 'Up':
            self.active_brick.rotate()
        elif command == 'Down':
            self.active_brick.move_down()
        elif command == 'space':
            self._hard_drop()

    def _find_full_lines(self):
        full_lines = []
        for i, row in enumerate(self.tiles):
            if (set(row) & self.bricks) == set(row):
                full_lines.append(i)
        return full_lines

    def _remove_full_lines(self, full_lines):
        for line in sorted(full_lines):
            self.bricks -= set(self.tiles[line])
            for row in range(line, 1, -1):
                for i, tile in enumerate(self.tiles[row]):
                    tile_above = self.tiles[row - 1][i]
                    if tile_above in self.active_brick.tiles:
                        continue
                    elif tile_above.has_brick:
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

    def _tick(self):
        if not self.active:
            return
        elif self.active_brick.can_move_down:
            self.active_brick.move_down()
        else:
            self.spawn_next_brick()
        self.app.after(self.tick_time, self._tick)

    def _hard_drop(self):
        while self.active_brick.can_move_down:
            self.active_brick.move_down()
        self.spawn_next_brick()

    def is_collision(self, new_coordinates):
        tiles_to_check = {self.tiles[r][c]
                          for r, c in new_coordinates}
        return bool(self.bricks & tiles_to_check)
