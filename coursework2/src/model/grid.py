from model.square import Square, Percept

from dataclasses import dataclass, field
from pyre_extensions import override
from typing import ClassVar, Self


@dataclass
class Grid:
    """Class to store the state of a Grid problem"""

    grid_size: int
    squares: list[Square] = field(init=False)
    current: Square = field(init=False)
    stack: list[tuple[int, int]] = field(default_factory=list)
    route: list[tuple[int, int]] = field(default_factory=list)
    safe: set[tuple[int, int]] = field(default_factory=set)
    risks: set[tuple[int, int]] = field(default_factory=set)
    hazards: set[tuple[int, int]] = field(default_factory=set)
    filippos: set[tuple[int, int]] = field(default_factory=set)
    python_books: int = 1  # Can only use Python book once
    _grid_: ClassVar[Self] = None  # Used for 'singleton'

    def __post_init__(self) -> None:
        """Setup grid and initial state"""

        self.squares = [
            Square(x, y, self.grid_size)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        ]
        self.current = self.get_square(0, 0)
        self.stack.append(self.current.coords)
        self.route.append(self.current.coords)
        self.safe.add(self.current.coords)

    def move_to(self, to: Square) -> str:
        """Moves to a new square"""

        from_coords = self.current.coords
        to_coords = to.coords
        print(f"Moving from {from_coords} to {to_coords}")

        # Update state
        self.current.unexplored.discard(to_coords)
        self.stack.append(to_coords)
        self.route.append(to_coords)
        self.safe.add(to_coords)

        self.current = to
        self.current.unexplored.discard(from_coords)
        return to.relative_to(from_coords)

    def back(self) -> str:
        """Moves back to previous square"""

        from_coords = self.stack.pop()
        to_coords = self.stack[-1]
        print(f"Moving from {from_coords} to {to_coords}")

        self.route.append(to_coords)
        self.current = self.get_square(*to_coords)
        return self.current.relative_to(from_coords)

    # def is_path_explored(self) -> bool:
    #     """Determines whether there is an unexplored branch from a previous square"""
    #
    #     for xy in reversed(self.stack[:-1]):
    #         if self.get_square(*xy).unexplored:
    #             print(f"Square at {xy} not fully explored.")
    #             return False
    #     return True

    def safe_path(self) -> bool:
        """Determines whether there is a safe route from a previous square in the stack"""

        for xy in reversed(self.stack[:-1]):
            unexplored = self.get_square(*xy).unexplored
            if any(s in self.safe for s in unexplored):
                print(f"Square at {xy} has possible route.")
                return True
        return False

    def _update_risks(self) -> None:
        """Updates the potential risks"""

        for square in self.squares:
            if len(square.percepts):
                self.risks.update(
                    [s for s in square.unexplored if s not in self.safe]
                )
        self.risks.difference_update(self.safe)

    def _update_hazards(self) -> None:
        """Updates the known hazards"""

        for square in self.squares:
            if len(square.percepts) == len(square.unexplored):
                self.hazards.update(square.unexplored)

    def update_percepts(self, percept: str) -> None:
        """Updates state of the grid according to the new percepts"""

        percepts = [Percept[p.upper()] for p in percept]
        self.current.percepts = percepts

        self.safe.add(self.current.coords)
        self._update_risks()
        self._update_hazards()

        if Percept.DRONING in percepts:
            unsafe = [r for r in self.current.options if r not in self.safe]
            # If there have already been Filippos percepts...
            if len(self.filippos):
                # Reduce possible locations to common squares
                self.filippos = self.filippos & set(unsafe)
            else:
                self.filippos = set(unsafe)

        if Percept.BORING in percepts:
            self.risks.update(
                [r for r in self.current.options if r not in self.safe]
            )

        # Remove known hazards as potential moves
        for square in self.squares:
            square.options.difference_update(self.hazards)

    def get_square(self, x: int, y: int) -> Square | None:
        """Gets a square from the grid using supplied coordinates"""

        return next(
            filter(lambda s: s.x == x and s.y == y, self.squares),
            None
        )

    def safe_options(self, percept: Percept) -> set[tuple[int, int]]:
        """Finds potentially safe squares by comparing previous percepts"""

        safe_options = set()
        for xy in [s for s in self.route if s != self.current.coords]:
            risks = self.current.shared_percepts(self.get_square(*xy), percept)
            if risks:
                potential = [s for s in risks if s not in self.route]
                for s in potential:
                    print(f"Book might be at {s}. ", end="")
                    safe_options.update([o for o in self.current.unexplored if not o == s])
                print(f"Potentially safe options are: {safe_options}")
        return safe_options

    @override
    def __str__(self):
        """Returns Grid state"""

        return (
            f"Hazards: {self.hazards or None}\n"
            f"Risks: {self.risks or None}\n"
            f"Filippos: {self.filippos or None}\n"
            f"Safe: {self.safe or None}\n"
            f"Unknown: {self.current.unexplored or None}\n"
            f"Options: {self.current.options or None}\n"
            f"Stack: {self.stack}\n"
            f"Route: {self.route}\n"
        )

    @classmethod
    def grid(cls, size: int):
        """Pseudo-singleton class method for Grid"""

        if not cls._grid_:
            cls._grid_ = cls(size)
        return cls._grid_
