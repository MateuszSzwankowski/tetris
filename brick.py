import numpy as np
import random


class Brick:
    # first point is a pivot used in brick rotation
    BRICK_TYPES = [{'color': 'cyan',    'init_pos': np.array([[1, 5], [1, 3], [1, 4], [1, 6]])},  # I
                   {'color': 'yellow',  'init_pos': np.array([[1, 4], [1, 5], [0, 4], [0, 5]])},  # O
                   {'color': 'magenta', 'init_pos': np.array([[0, 4], [0, 3], [0, 5], [1, 4]])},  # T
                   {'color': 'green',   'init_pos': np.array([[1, 4], [0, 4], [0, 5], [1, 3]])},  # S
                   {'color': 'red',     'init_pos': np.array([[1, 4], [0, 3], [0, 4], [1, 5]])},  # Z
                   {'color': 'blue',    'init_pos': np.array([[1, 4], [0, 3], [1, 5], [1, 3]])},  # J
                   {'color': 'orange',  'init_pos': np.array([[1, 4], [0, 5], [1, 3], [1, 5]])}]  # L
    brick_queue = []

    def __init__(self, board):
        self.board = board
        # refill queue if empty
        if not Brick.brick_queue:
            Brick.brick_queue = random.sample(Brick.BRICK_TYPES,
                                              len(Brick.BRICK_TYPES))
        new_brick = Brick.brick_queue.pop()
        self.color = new_brick['color']
        self.coords = new_brick['init_pos'].copy()

        self.tiles = {self.board.tiles[r][c] for r, c in self.coords}
        self.dropping = False

    def redraw(self):
        if self.tiles == {self.board.tiles[r][c] for r, c in self.coords}:
            return
        
        for tile in self.tiles:
            tile.has_brick = False
            tile['image'] = self.board.images[tile.default_color]

        self.tiles = {self.board.tiles[r][c] for r, c in self.coords}

        for tile in self.tiles:
            tile['image'] = self.board.images[self.color]
            tile.has_brick = True

    def move_down(self):
        self.coords[:, 0] += 1
        if not self._can_move_to(self.coords):
            self.coords[:, 0] -= 1
            self.board.spawn_next()
        else:
            self.redraw()

    def move_right(self):
        self.coords[:, 1] += 1
        if not self._can_move_to(self.coords):
            self.coords[:, 1] -= 1
        else:
            self.redraw()

    def move_left(self):
        self.coords[:, 1] -= 1
        if not self._can_move_to(self.coords):
            self.coords[:, 1] += 1
        else:
            self.redraw()

    def rotate(self):
        if self.color == 'yellow':  # square does not rotate
            return

        pivot = self.coords[0].copy()
        self.coords -= pivot

        c1 = (self.coords[:, 0] * np.cos(np.pi/2)
              - self.coords[:, 1] * np.sin(np.pi/2))
        c2 = (self.coords[:, 0] * np.sin(np.pi/2)
              + self.coords[:, 1] * np.cos(np.pi/2))
        new_coords = np.column_stack((c1, c2)).round().astype(int)
        new_coords += pivot

        if self._can_move_to(new_coords):
            self.coords = new_coords
            self.redraw()
        else:
            self.coords += pivot

    def _can_move_to(self, new_coordinates):
        return (np.max(new_coordinates[:, 0]) < self.board.BOARD_HEIGHT
                and np.min(new_coordinates[:, 0]) >= 0
                and np.max(new_coordinates[:, 1]) < self.board.BOARD_WIDTH
                and np.min(new_coordinates[:, 1]) >= 0
                and not self.board.is_collisions(new_coordinates))
