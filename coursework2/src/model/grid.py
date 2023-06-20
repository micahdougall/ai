from logger import Logger
from model.bayes import bayes_probability
from model.square import Percept, State, Square

from dataclasses import dataclass, field
from functools import reduce
from more_itertools import one
from operator import mul
from pyre_extensions import override


@dataclass
class Grid:
    """Class to store the state of a Grid problem"""

    grid_size: int
    book_count: int = 4
    squares: list[Square] = field(init=False)
    current: Square = field(init=False)
    stack: list[tuple[int, int]] = field(default_factory=list)
    route: list[tuple[int, int]] = field(default_factory=list)
    filippos: set[tuple[int, int]] = field(default_factory=set)
    python_books: int = 1  # Can only use Python book once
    logger: Logger = field(init=False)

    def __post_init__(self) -> None:
        self.squares = [
            Square(x, y, self.grid_size, self.book_count)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        ]
        start_coords = (0, 0)
        self.current = self.get_square(*start_coords)
        self.stack.append(start_coords)
        self.logger = Logger.logger()

    @property
    def visited(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.VISITED
        }

    @property
    def safe(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.SAFE
        }

    @property
    def all_safe(self) -> set[tuple[int, int]]:
        return self.safe.union(self.visited)

    @property
    def unknown(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.UNKNOWN
        }
    
    @property
    def viable(self) -> set[tuple[int, int]]:
        return self.all_safe.union(self.unknown)

    @property
    def books(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.BOOK
        }

    @property
    def risks(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.RISK
        }

    @property
    def hazards(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state in [
                State.BOOK, State.FILIPPOS
            ]
        }

    def get_square(self, x: int, y: int) -> Square | None:
        """Gets a square from the grid using supplied coordinates.

        Args:
            x: x-coordinate.
            y: y-coordinate.

        Returns:
            A Square if one exists in the Grid with the given coordinates
            else None.
        """

        return next(
            filter(lambda s: s.x == x and s.y == y, self.squares),
            None
        )

    def move_to(self, to_coords: tuple[int, int]) -> str:
        """Updates the grid state to a new square.

        Args:
            to_coords: the coordinate to move to.

        Returns:
            the string value for the move direction required.
        """

        from_coords = self.current.coords
        self.logger.log(f"Moving from {from_coords} to {to_coords}")

        # Update state
        self.stack.append(to_coords)
        self.current = self.get_square(*to_coords)

        return self.current.relative_to(from_coords)

    def back(self) -> str:
        """Updates the grid state to the previous square.

        Returns:
            the move direction relative to the current square as a string.
        """

        from_coords = self.stack.pop()
        to_coords = self.stack[-1]
        self.logger.log(f"Moving from {from_coords} to {to_coords}")

        self.current = self.get_square(*to_coords)
        return self.current.relative_to(from_coords)

    def safe_unexplored_path(self) -> bool:
        """Determines whether there is a safe route from a
        previous square in the stack.

        Returns:
            True if there is an unexplored safe route from a
            previous square, else False.
        """

        for xy in reversed(self.stack[:-1]):
            if any(
                self.get_square(*s).state == State.SAFE
                for s in self.get_square(*xy).options
            ):
                self.logger.log(f"Square at {xy} has a safe option.")
                return True
        return False

    def safest_options(self, percept: Percept) -> set[tuple[int, int]]:
        """Finds potentially safe squares by comparing previous percepts

        Args:
            percept:

        Returns:

        """
        options = self.current.options.difference(
            self.visited, self.hazards
        )
        for xy in self.visited.difference({self.current.coords}):
            shared = self.current.shared_percepts(
                self.get_square(*xy), 
                percept
            )
            if shared:
                likely = shared.difference(self.all_safe)
                self.logger.log(f"Book might be at one of {likely}. ")
                options.difference_update(likely)
        self.logger.log(f"Potentially safe options are: {options}")
        return options
    
    def update_states(self, percepts: list[str]) -> None:
        """Updates the Grid states according to perceptions.

        Args:
            percepts: list of percepts received from CWorld for the
            current square.
        """
        if not self.current.state == State.VISITED:
            self.current.state = State.VISITED
            if not percepts:
                self.logger.log(f"No percept, updating adjacent square states to safe")
                for s in self.current.options.difference(
                    self.visited
                ):
                    self.get_square(*s).state = State.SAFE
            else:
                self._update_percepts(percepts)

    def _update_percepts(self, percept_list: list[str]) -> None:
        """Updates state of the grid according to the new percepts

        Args:
            percept_list: list of percepts received from CWorld for the
            current square.
        """

        percepts = [Percept[p.upper()] for p in percept_list]
        self.current.percepts = percepts

        # Deal with Filippos
        if Percept.DRONING in percepts:
            potentials = self.current.options.difference(
                self.all_safe.union(self.books)
            )
            if len(self.filippos):
                # Reduce possible locations to common squares
                self.filippos = self.filippos & set(potentials)
            else:
                self.filippos = potentials

            # If only one possibility, confirm as Filippos
            if len(self.filippos) == 1:
                self.get_square(
                    *one(self.filippos)
                ).state = State.FILIPPOS

        if Percept.BORING in percepts:
            book_count = len([p for p in percepts if p == Percept.BORING])

            # If number of books equals the remaining squares (adjacent)
            # then update them all to books.
            potential_books = self.current.options.intersection(
                self.unknown.union(self.books, self.risks, self.unknown)
            )
            # if len(potential_books) == book_count:
            for s in potential_books:
                square = self.get_square(*s)
                square.state = (
                    State.BOOK
                    if len(potential_books) == book_count
                    else State.RISK
                ) if square.state != State.FILIPPOS else square.state

    def update_probabilities(self) -> None:
        if Percept.BORING in self.current.percepts:
            for square in self.current.options:
                self._book_probability(
                    self.get_square(*square)
                )
        if Percept.DRONING in self.current.percepts:
            for square in self.current.options:
                self._filippos_probability(
                    self.get_square(*square)
                )

    # def square_probability(self, square: Square, prior: float = None) -> float:
    def _book_probability(self, square: Square) -> float:
        
        # Allows for prior=0 as named arg
        # prior = square.book_probability if prior is None else prior

        # Specificity equates to the cominbed likelihood of all other
        # adjacent squares being safe, so that a negative result
        # would be given (ie. no percept). 
        square_probabilities = [
            (1 - self.get_square(*s).book_prob) for s in square.options
        ]
        specificity = reduce(mul, square_probabilities)

        # Uses square's prior probability
        # return bayes_probability(square.book_prob, specificity)
        prob = bayes_probability(square.book_prob, specificity)
        print(f"Updated {square.book_prob} probability to {prob}")
        square.book_prob = prob

    def _filippos_probability(self, square: Square) -> float:
        
        # Specificity equates to the combined likelihood of all other
        # adjacent squares being safe, so that a negative result
        # would be given (ie. no percept). 
        square_probabilities = [
            (1 - self.get_square(*s).filippos_prob) for s in square.options
        ]
        specificity = reduce(mul, square_probabilities)

        # Uses square's prior probability
        prob = bayes_probability(square.filippos_prob, specificity)
        print(f"Updated F {square.filippos_prob} probability to {prob}")
        square.filippos_prob = prob

    @override
    def __str__(self):
        return "\t" + "\n\t".join([str(s) for s in self.squares])
