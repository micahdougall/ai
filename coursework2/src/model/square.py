from dataclasses import dataclass, field, InitVar, asdict
from enum import Enum
from typing import Self


# TODO: Is this still needed?
Percept = Enum('Percept', 'BORING DRONING SUCCESS')


@dataclass
class Square:
    x: int
    y: int
    grid_size: InitVar[int]
    coords: Self = field(init=False)
    up: Self = field(init=False)
    down: Self = field(init=False)
    left: Self = field(init=False)
    right: Self = field(init=False)
    options: list[Self] = None
    unknowns: list[Self] = None
    percepts: list[Percept] = None

    def __post_init__(self, grid_size):
        self.coords = self.x, self.y
        self.up = (self.x - 1, self.y) if self.x > 0 else None
        self.down = (self.x + 1, self.y) if self.x < grid_size - 1 else None
        self.left = (self.x, self.y - 1) if self.y > 0 else None
        self.right = (self.x, self.y + 1) if self.y < grid_size - 1 else None

        self.options = self.unknowns = list(
            filter(None, [self.up, self.down, self.left, self.right])
        )

    def is_explored(self) -> bool:
        return len(self.unknowns) == 0

    def dir_from(self, other: tuple[int, int]) -> str:
        x, y = other
        return {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right"
        }.get((self.x - x, self.y - y))
