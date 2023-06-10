from typing import ClassVar, Self
import sys

# if "square" not in sys.modules:
from coursework2.src.model.square import Square
# else:
#     print(sys.modules)
# import coursework2.src.model.square as s

from dataclasses import dataclass, field, InitVar, asdict


# from enum import Enum

# Percept = Enum('Percept', 'BORING DRONING SUCCESS')


@dataclass
class Grid:
    grid_size: int
    # options: list[Square] = None
    # unknowns: list[Square] = None
    squares: list[Square] = field(init=False)
    current: Square = field(init=False)
    stack: list[Square] = field(default_factory=list)
    route: list[Square] = field(default_factory=list)
    # up: Square = field(init=False)
    # down: Square = field(init=False)
    # left: Square = field(init=False)
    # right: Square = field(init=False)
    # options: list[Square] = field(init=False)
    # unknowns: list[Square] = field(init=False)
    # returned: bool = False
    # last_move: str = None
    # map: dict[tuple, str] = {}
    _grid_: ClassVar[Self] = None

    def __post_init__(self):
        # coords = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        test = [
            # Square(*xy, self.grid_size) for xy in coords
            (x, y)
            for x in range(4)
            for y in range(4)
        ]
        # print(test)
        self.squares = [
            # s.Square(*xy, self.grid_size) for xy in coords
            Square(t[0], t[1], self.grid_size)
            # for x in range(self.grid_size)
            # for x in range(4)
            # for y in range(self.grid_size)
            # for y in range(4)
            for t in test
        ]
        # print(self)
        # exit()
        # for square in self.squares:
        #     print(square)
            # square.up = self.get_square(square.x - 1, square.y) if square.x > 0 else None
            # square.down = self.get_square(square.x + 1, square.y) if square.x < self.grid_size - 1 else None
            # square.left = self.get_square(square.x, square.y - 1) if square.y > 0 else None
            # square.right = self.get_square(square.x, square.y + 1) if square.y < self.grid_size - 1 else None
            # print("added dirs")
            # square.options = square.unknowns = list(
            #     filter(None, [square.up, square.down, square.left, square.right])
            # )
            # print(square)
            # print("done options")

        # print("ok")
        # exit()
        self.current = self.get_square(0, 0)
        # print("current is done")
        # print(self.current)
        # print("current is done printing")
        self.stack.append(self.current.coords)
        # print(self.stack)
        # print("stack is done")

        # def __post_init__(self, grid_size):
            # self.options = self.unknowns = {
            #     k: v for (k, v) in self.map_moves(grid_size).items() if v
            # }
            # for attr in ["up", "down", "left", "right"]:
            #     setattr(self, attr, moves(attr))
            # grid = g.Grid.grid(grid_size)
            # grid_size = grid.grid_size
            # self.x = 1
        # self.up = self.get_square(self.current.x - 1, self.current.y) if self.current.x > 0 else None
        # self.down = self.get_square(self.current.x + 1, self.current.y) if self.current.x < self.grid_size - 1 else None
        # self.left = self.get_square(self.current.x, self.current.y - 1) if self.current.y > 0 else None
        # self.right = self.get_square(self.current.x, self.current.y + 1) if self.current.y < self.grid_size - 1 else None

        # self.options = self.unknowns = list(
        #     filter(None, [self.up, self.down, self.left, self.right])
        # )


            # Square(v) for (k, v) in asdict(self).items() if k in ("up", "down", "left", "right") and v
        # ]
        # print(self)
        # exit()

    def move(self, direction: str):
        move = moves_coords_map(self.current.x, self.current.y, self.grid_size).get(direction)
        if move:
            to = self.get_square(move[0], move[1])
            self.current.unknowns.remove(to)
            self.current = to
            self.stack.append(to.coords)
            self.route.append(to.coords)

    def move_to(self, to: Square):
        print(f"Stack before move: {self.stack}")
        print(f"Unknown before move: {self.current.unknowns}")
        # exit()
        # print(to)
        # print(type(to))
        self.current.unknowns.remove(to.coords)
        self.current = to
        self.stack.append(to.coords)
        print(f"Stack after append: {self.stack}")
        self.route.append(to.coords)
        return to.dir_from(self.stack[-2])

    def back(self) -> str:
        current = self.stack.pop()
        return self.get_square(*self.stack[-1]).dir_from(current)

    def get_square(self, x: int, y: int) -> Square | None:
        # for s in self.squares:
        #     if s.x == x and s.y == y:
        #         print("Found")
        #         print(s)
        #         return s
        # return None
        return next(
            filter(lambda s: s.x == x and s.y == y, self.squares),
            None
        )

    @classmethod
    def grid(cls, size: int):
        """Pseudo-singleton class method for Grid"""
        if not cls._grid_:
            cls._grid_ = cls(size)
        return cls._grid_

    def is_explored(self) -> bool:
        return len(self.unknowns) == 0

    # def dir_from(self, other: Self) -> str:
    #     return {
    #         (-1, 0): "up",
    #         (1, 0): "down",
    #         (0, -1): "left",
    #         (0, 1): "right"
    #     }.get((self.x - other.x, self.y - other.y))


def moves_coords_map(x: int, y: int, grid_size) -> dict:
    return {
        "up": (x - 1, y) if x > 0 else None,
        "down": (x + 1, y) if x < grid_size - 1 else None,
        "left": (x, y - 1) if y > 0 else None,
        "right": (x, y + 1) if y < grid_size - 1 else None,
    }

# def moves_coords_map(x: int, y: int, grid_size) -> dict:
#     return {
#         "up": (x - 1, y) if x > 0 else None,
#         "down": (x + 1, y) if x < grid_size - 1 else None,
#         "left": (x, y - 1) if y > 0 else None,
#         "right": (x, y + 1) if y < grid_size - 1 else None,
#     }
# def opposite(move: str) -> str:
#     return {
#         "up": "down",
#         "down": "up",
#         "left": "right",
#         "right": "left",
#     }.get(move)

