from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Self

Percept = Enum('Percept', 'BORING DRONING SUCCESS')
Risk = Enum('Risk', 'BOOK FILIPPOS')
State = Enum('State', 'UNKNOWN SAFE VISITED BOOK FLIPPOS')


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
    options: set[tuple[int, int]] = field(default_factory=set)
    unexplored: set[tuple[int, int]] = field(default_factory=set)
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
        self.options = set(
            filter(None, {self.up, self.down, self.left, self.right})
        )
        self.unexplored = self.options.copy()
        # self.safe = False
        self.book_prob = book_count / pow(grid_size, 2)

    @property
    def state(self) -> State:
        return self._state
        # return (
        #     self.book_prob == 0 and self.filippos_prob == 0
        # )

    @state.setter
    def state(self, state: State) -> None:
        if state == State.SAFE:
            self.book_prob = 0
            self.filippos_prob = 0
        self._state = State.SAFE

    # @safe.setter
    # def safe(self, is_safe: bool, risk_type: Percept = None) -> None:
    #     if not is_safe:
    #         if risk_type is None:
    #             raise ValueError(
    #                 "Missing 'risk_type' for setter 'safe' when 'is_safe=False'"
    #             )
    #         elif risk_type == Risk.FILIPPOS:

    def relative_to(self, other: tuple[int, int]) -> str:
        """Gets the relative direction of another square as a string"""

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
        """Returns the adjacent squares which are common to both squares if a percept exists"""

        return (
            set(self.options) & set(other.options) 
            if percept in other.percepts 
            else None
        )
    
    def __str__(self) -> str:
        return f"{self.coords} -> ({self.state.name}) -> {self.book_prob}"
