from typing import ClassVar, Self
import sys

# if "square" not in sys.modules:
#     from coursework2.src.model.square import s.Square
# else:
#     print(sys.modules)
import coursework2.src.model.square as s

from dataclasses import dataclass, field, InitVar
# from enum import Enum

# Percept = Enum('Percept', 'BORING DRONING SUCCESS')


@dataclass
class Grid:
    grid_size: int
    squares: list[s.Square] = field(init=False)
    current: s.Square = field(init=False)
    stack: list[s.Square] = field(default_factory=list)
    route: list[s.Square] = field(default_factory=list)
    up: Self = field(init=False)
    down: Self = field(init=False)
    left: Self = field(init=False)
    right: Self = field(init=False)
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
        print(test)
        self.squares = [
            # s.Square(*xy, self.grid_size) for xy in coords
            s.Square(t[0], t[1], self.grid_size)
            # for x in range(self.grid_size)
            # for x in range(4)
            # for y in range(self.grid_size)
            # for y in range(4)
            for t in test
        ]
        self.current = self.get_square(0, 0)

    def move(self, direction: str):
        move = moves_coords_map(self.current.x, self.current.y, self.grid_size).get(direction)
        if move:
            to = self.get_square(move[0], move[1])
            self.current.unknowns.remove(to)
            self.current = to
            self.stack.append(to)
            self.route.append(to)

    def move_to(self, to: s.Square):
        self.current.unknowns.remove(to)
        self.current = to
        self.stack.append(to)
        self.route.append(to)
        return to.dir_from(self.stack[-2])

    def back(self) -> str:
        current = self.stack.pop()
        return self.stack[-1].dir_from(current)

    def get_square(self, x: int, y: int) -> s.Square | None:
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


def moves_coords_map(x: int, y: int, grid_size) -> dict:
    return {
        "up": (x - 1, y) if x > 0 else None,
        "down": (x + 1, y) if x < grid_size - 1 else None,
        "left": (x, y - 1) if y > 0 else None,
        "right": (x, y + 1) if y < grid_size - 1 else None,
    }
# def opposite(move: str) -> str:
#     return {
#         "up": "down",
#         "down": "up",
#         "left": "right",
#         "right": "left",
#     }.get(move)

