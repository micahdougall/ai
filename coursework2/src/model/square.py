from model.enums import Percept, State

from dataclasses import InitVar, dataclass, field
from pyre_extensions import override
from typing import Self


@dataclass
class Square:
    """Class to store the state of a Square in a Grid problem"""

    x: int
    y: int
    grid_size: InitVar[int]
    book_count: InitVar[int]
    coords: tuple[int, int] = field(init=False)
    up: tuple[int, int] = field(init=False)
    down: tuple[int, int] = field(init=False)
    left: tuple[int, int] = field(init=False)
    right: tuple[int, int] = field(init=False)
    percepts: list[Percept] = field(default_factory=list)
    book_prob: float = field(init=False)
    filippos_prob: float = field(init=False)
    _state: State = State.UNKNOWN

    def __post_init__(self, grid_size, book_count) -> None:
        """Setup relative coordinates and initial state"""

        self.coords = self.x, self.y
        self.up = (self.x - 1, self.y) if self.x > 0 else None
        self.down = (self.x + 1, self.y) if self.x < grid_size - 1 else None
        self.left = (self.x, self.y - 1) if self.y > 0 else None
        self.right = (self.x, self.y + 1) if self.y < grid_size - 1 else None
        self.book_prob = book_count / pow(grid_size, 2)
        self.filippos_prob = 1 / pow(grid_size, 2)

    @property
    def options(self) -> set[tuple[int, int]]:
        return set(
            filter(None, {self.up, self.down, self.left, self.right})
        )
    
    @property
    def risk(self) -> float:
        return self.book_prob + self.filippos_prob

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        if state in [State.SAFE, State.VISITED]:
            self.book_prob = 0
            self.filippos_prob = 0
        elif state == State.BOOK:
            self.filippos_prob = 0
            self.book_prob = 1
        elif state == State.FILIPPOS:
            self.filippos_prob = 1
            self.book_prob = 0
        self._state = state

    def relative_to(self, other: tuple[int, int]) -> str:
        """Gets the relative direction of another square as a string

        Args:
            other: the other coordinates to determine the move to.

        Returns:
            a string representation of the direction required to move.
        """

        x, y = other
        return {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right"
        }.get((self.x - x, self.y - y))

    def shared_percepts(
            self, other: Self, percept: Percept
    ) -> set[tuple[int, int]] | None:
        """Returns the adjacent squares which are common to both squares if a percept exists

        Args:
            other: the other Square to compare percepts with.
            percept: the percept to compare.

        Returns:
            a set of coordinates which are shared between the two squares.
        """

        return (
            set(self.options) & set(other.options) 
            if percept in other.percepts 
            else None
        )

    @override
    def __str__(self) -> str:
        return f"{self.coords} -> ({self.state.name}) -> {self.book_prob}"
