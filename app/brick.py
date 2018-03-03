import numpy as np


class Brick:

    brick_queue = []

    def __init__(self, board, brick_type):
        self.board = board

        self.type = brick_type['type']
        self.color = brick_type['color']
        self.coords = brick_type['init_pos'].copy()

        self.tiles = {self.board.tiles[r][c] for r, c in self.coords}

    @property
    def can_move_down(self):
        new_coords = self.coords.copy()
        new_coords[:, 0] += 1
        return self._can_move_to(new_coords)

    def move_down(self):
        new_coords = self.coords.copy()
        new_coords[:, 0] += 1
        if self._can_move_to(new_coords):
            self._move_to(new_coords)

    def move_right(self):
        new_coords = self.coords.copy()
        new_coords[:, 1] += 1
        if self._can_move_to(new_coords):
            self._move_to(new_coords)

    def move_left(self):
        new_coords = self.coords.copy()
        new_coords[:, 1] -= 1
        if self._can_move_to(new_coords):
            self._move_to(new_coords)

    def rotate(self):
        if self.type == 'O':  # square does not rotate
            return

        pivot = self.coords[0].copy()
        self.coords -= pivot

        row_vector = -self.coords[:, 1]
        column_vector = self.coords[:, 0]
        new_coords = np.column_stack((row_vector, column_vector))
        new_coords += pivot

        if self._can_move_to(new_coords):
            self._move_to(new_coords)
        else:
            self.coords += pivot

    def _can_move_to(self, new_coordinates):
        return (np.max(new_coordinates[:, 0]) < self.board.BOARD_HEIGHT
                and np.min(new_coordinates[:, 0]) >= 0
                and np.max(new_coordinates[:, 1]) < self.board.BOARD_WIDTH
                and np.min(new_coordinates[:, 1]) >= 0
                and not self.board.is_collision(new_coordinates))

    def _move_to(self, new_coords):
        if not (self.coords - new_coords).any():
            return  # old and new coordinates are equal

        self.coords = new_coords
        for tile in self.tiles:
            tile.has_brick = False
            tile['image'] = self.board.images[tile.default_color]

        self.tiles = {self.board.tiles[r][c] for r, c in self.coords}

        for tile in self.tiles:
            tile.has_brick = True
            tile['image'] = self.board.images[self.color]
