from grid import Grid
from square import Square

from dataclasses import dataclass, field, InitVar


@dataclass
class Map:
    up: Square
    down: Square
    left: Square
    right: Square

    def __int__(self, x, y):
        grid = Grid.grid()
        grid_size = grid.grid_size

        self.up: grid.get_square(x - 1, y) if x > 0 else None
        self.down: grid.get_square(x + 1, y) if x < grid_size - 1 else None
        self.left: grid.get_square(x, y - 1) if y > 0 else None
        self.right: grid.get_square(x, y + 1) if y < grid_size - 1 else None