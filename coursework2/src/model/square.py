from typing import Self

# from map import Map

from dataclasses import dataclass, field, InitVar, asdict
from enum import Enum
import sys

# from grid import Grid
import coursework2.src.model.grid as g

# if "grid" not in sys.modules:
#     import coursework2.src.model.grid as g
    #
    # from coursework2.src.model.grid import Gr
# else:
#     print(sys.modules)

Percept = Enum('Percept', 'BORING DRONING SUCCESS')


@dataclass
class Square:
    x: int
    y: int
    grid_size: InitVar[int]
    # neighbours: Map
    # up: Self = field(init=False)
    # down: Self = field(init=False)
    # left: Self = field(init=False)
    # right: Self = field(init=False)
    options: list[Self] = field(init=False)
    unknowns: list[Self] = field(init=False)
    percepts: list[Percept] = field(init=False)

    # def __post_init__(self, grid_size: int):
    def __post_init__(self, grid_size):
        # self.options = self.unknowns = {
        #     k: v for (k, v) in self.map_moves(grid_size).items() if v
        # }
        # for attr in ["up", "down", "left", "right"]:
        #     setattr(self, attr, moves(attr))
        # grid = g.Grid.grid(grid_size)
        # grid_size = grid.grid_size
        # self.x = 1
        self.up = grid.get_square(self.x - 1, self.y) if self.x > 0 else None
        self.down = grid.get_square(self.x + 1, self.y) if self.x < grid_size - 1 else None
        self.left = grid.get_square(self.x, self.y - 1) if self.y > 0 else None
        self.right = grid.get_square(self.x, self.y + 1) if self.y < grid_size - 1 else None

        self.options = self.unknowns = [
            v for (k, v) in asdict(self).values() if k in ("up", "down", "left", "right")
        ]

    # def moves(self, direction: str) -> dict:
    #     return {
    #         "up": (x - 1, y) if x > 0 else None,
    #         "down": (x + 1, y) if x < grid_size - 1 else None,
    #         "left": (x, y - 1) if y > 0 else None,
    #         "right": (x, y + 1) if y < grid_size - 1 else None,
    #     }.get(direction)

    # def __int__(self, x, y):
    #     grid = Grid.grid()
    #     grid_size = grid.grid_size
    #
    #     self.up: grid.get_square(x - 1, y) if x > 0 else None
    #     self.down: grid.get_square(x + 1, y) if x < grid_size - 1 else None
    #     self.left: grid.get_square(x, y - 1) if y > 0 else None
    #     self.right: grid.get_square(x, y + 1) if y < grid_size - 1 else None

    def is_explored(self) -> bool:
        return len(self.unknowns) == 0

    def dir_from(self, other: Self) -> str:
        return {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right"
        }.get((self.x - other.x, self.y - other.y))


def moves_coords_map(x: int, y: int, grid_size) -> dict:
    return {
        "up": (x - 1, y) if x > 0 else None,
        "down": (x + 1, y) if x < grid_size - 1 else None,
        "left": (x, y - 1) if y > 0 else None,
        "right": (x, y + 1) if y < grid_size - 1 else None,
    }




