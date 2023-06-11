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
    coords: tuple[int, int] = field(init=False)
    up: Self = field(init=False)
    down: Self = field(init=False)
    left: Self = field(init=False)
    right: Self = field(init=False)
    options: list[Self] = field(default_factory=list)
    # safe: list[Self] = field(default_factory=list)
    unknowns: list[Self] = field(default_factory=list)
    percepts: list[Percept] = field(default_factory=list)

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
        print(f"Is explored? Options at {self.coords} = {self.unknowns}")
        return len(self.unknowns) == 0

    def relative_to(self, other: tuple[int, int]) -> str:
        x, y = other
        return {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right"
        }.get((self.x - x, self.y - y))

    # def is_diagonal(self, other: tuple[int, int]) -> bool:
    def is_diagonal(self, x: int, y: int) -> bool:
        # x, y = other
        return abs(self.x - x) == 1 and abs(self.y - y) == 1

    def shared_adjacents(self, other: Self) -> list[tuple[int, int]]:
        """Returns the adjacent square which are common to both squares"""
        # x, y = other
        return list(set(self.options) and set(other.options))
        # return abs(self.x - x) == 1 and abs(self.y - y) == 1

    # TODO: Enum for percept
    def shared_percepts(self, other: Self, percept: str) -> list[tuple[int, int]]:
        """Returns the adjacent square which are common to both squares"""
        # print(f"Self is {self.coords} with options: {self.options}")
        # x, y = other
        # if other.percepts.
        return list(set(self.options) & set(other.options)) if percept in other.percepts else None
        # return abs(self.x - x) == 1 and abs(self.y - y) == 1


