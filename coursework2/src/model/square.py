from dataclasses import dataclass, field, InitVar
from enum import Enum
from typing import Self


Percept = Enum('Percept', 'BORING DRONING SUCCESS')


@dataclass
class Square:
    """Class to store the state of a Square in a Grid problem"""

    x: int
    y: int
    grid_size: InitVar[int]
    coords: tuple[int, int] = field(init=False)
    up: tuple[int, int] = field(init=False)
    down: tuple[int, int] = field(init=False)
    left: tuple[int, int] = field(init=False)
    right: tuple[int, int] = field(init=False)
    options: set[tuple[int, int]] = field(default_factory=set)
    unexplored: set[tuple[int, int]] = field(default_factory=set)
    percepts: list[Percept] = field(default_factory=list)

    def __post_init__(self, grid_size) -> None:
        """Setup relative coordinates and initial state"""

        self.coords = self.x, self.y
        self.up = (self.x - 1, self.y) if self.x > 0 else None
        self.down = (self.x + 1, self.y) if self.x < grid_size - 1 else None
        self.left = (self.x, self.y - 1) if self.y > 0 else None
        self.right = (self.x, self.y + 1) if self.y < grid_size - 1 else None
        self.options = set(filter(None, {self.up, self.down, self.left, self.right}))
        self.unexplored = self.options.copy()

    def relative_to(self, other: tuple[int, int]) -> str:
        """Gets the relative direction of another square as a string"""

        x, y = other
        return {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right"
        }.get((self.x - x, self.y - y))

    def shared_percepts(self, other: Self, percept: Percept) -> set[tuple[int, int]] | None:
        """Returns the adjacent squares which are common to both squares if a percept exists"""

        return set(self.options) & set(other.options) if percept in other.percepts else None
