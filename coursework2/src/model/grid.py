from model.enums import Algorithm
from model.bayes import bayes_probability
from model.square import Percept, State, Square

from dataclasses import dataclass, field
from functools import reduce
from more_itertools import one
from operator import mul
# from typing import ClassVar, Self
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
    # safe: set[tuple[int, int]] = field(default_factory=set)
    # risks: set[tuple[int, int]] = field(default_factory=set)
    # hazards: set[tuple[int, int]] = field(default_factory=set)
    filippos: set[tuple[int, int]] = field(default_factory=set)
    python_books: int = 1  # Can only use Python book once
    # _grid_: ClassVar[Self] = None  # Used for 'singleton'

    def __post_init__(self) -> None:
        """Setup grid and initial state"""

        self.squares = [
            Square(x, y, self.grid_size, self.book_count)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        ]
        start_coords = (0, 0)
        self.current = self.get_square(*start_coords)
        self.stack.append(start_coords)
        # self.route.append(start_coords)
        # self.safe.add(self.current.coords)

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
    
    # @property
    # TODO: Risks as prop, simplify, 

    @property
    def unknown(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.UNKNOWN
        }

    @property
    def hazards(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state in [
                State.BOOK, State.FILIPPOS, State.HAZARD
            ]
        }

    @property
    def books(self) -> set[tuple[int, int]]:
        return {
            s.coords for s in self.squares if s.state == State.BOOK
        }

    def get_square(self, x: int, y: int) -> Square | None:
        """Gets a square from the grid using supplied coordinates"""

        return next(
            filter(lambda s: s.x == x and s.y == y, self.squares),
            None
        )

    def move_to(self, to_coords: tuple[int, int]) -> str:
        """Updates the grid state to a new square"""

        from_coords = self.current.coords
        # print(f"Moving from {from_coords} to {to_coords}")

        # Update state
        # self.current.unexplored.discard(to_coords)
        self.stack.append(to_coords)
        # self.route.append(to_coords)

        # self.safe.add(to_coords)
        # print(f"About to move, safe are: {self.safe}")

        self.current = self.get_square(*to_coords)
        # self.current.state = State.VISITED

        # self.current.unexplored.discard(from_coords)
        return self.current.relative_to(from_coords)

    def back(self) -> str:
        """Updates the grid state to the previous square and returns the move"""

        from_coords = self.stack.pop()
        to_coords = self.stack[-1]
        # print(f"Moving from {from_coords} to {to_coords}")

        # self.route.append(to_coords)
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

    def safe_unexplored_path(self) -> bool:
        """Determines whether there is a safe route from a previous square in the stack"""

        # for xy in reversed(self.stack[:-1]):
        #     unexplored = self.get_square(*xy).safe
        #     if any(s in self.safe for s in unexplored):
        #         print(f"Square at {xy} has possible route.")
        #         return True
        # return False

        for xy in reversed(self.stack[:-1]):
            if any(self.get_square(*s).state == State.SAFE for s in self.get_square(*xy).options):
                print(f"Square at {xy} has a safe option.")
                return True
        return False


    def safest_options(self, percept: Percept) -> set[tuple[int, int]]:
        """Finds potentially safe squares by comparing previous percepts"""

        options = self.current.options.difference(
            self.visited, self.hazards
        )
        # for xy in [s for s in self.route if s != self.current.coords]:
        for xy in self.visited.difference({self.current.coords}):
            shared = self.current.shared_percepts(
                self.get_square(*xy), 
                percept
            )
            if shared:
                possible = {
                    s for s in shared if self.get_square(*s).state in [
                        State.UNKNOWN, State.BOOK, State.FILIPPOS, State.HAZARD
                    ]
                }
                # for s in possible:
                print(f"Book might be at one of {possible}. ", end="")
                options.difference_update(possible)
                # options.update(
                    # [o for o in self.current.options if not o == s]
                # )
        print(f"Potentially safe options are: {options}")
        return options

    # def _update_risks(self) -> None:
    #     """Updates the potential risks"""

    #     for square in self.squares:
    #         if len(square.percepts):
    #             self.risks.update(
    #                 [s for s in square.unexplored if s not in self.safe]
    #             )
    #     self.risks.difference_update(self.safe)

    # def _update_hazards(self) -> None:
    #     """Updates the known hazards"""

    #     for square in self.squares:
    #         if len(square.percepts) == len(square.unexplored):
    #             self.hazards.update(square.unexplored)
    
    def update_states(self, percept: str) -> None:
        if not self.current.state == State.VISITED:
            self.current.state = State.VISITED
            if not percept:
                print(f"No percept, updating adjacents as safe")
                for s in self.current.options.difference(
                    self.visited
                ):
                    # self.grid.safe.add(s)
                    self.get_square(*s).state = State.SAFE
            else:
                self._update_percepts(percept)
                # TODO: Move this down
                # if self.algorithm == Algorithm.BAYES:
                #     self.log("Updating probabilities", warn=True, force=True)
                #     self._update_probabilities()

    def _update_percepts(self, percept: str) -> None:
        """Updates state of the grid according to the new percepts"""

        percepts = [Percept[p.upper()] for p in percept]
        self.current.percepts = percepts

        # self.safe.add(self.current.coords)
        # self.current.book_prob = 0
        # self.current.filippos_prob = 0
        # self.current.state = State.SAFE
        # self._update_risks()
        # self._update_hazards()

        print("Updating percepts...")

        if Percept.DRONING in percepts:
            potentials = [
                r for r in self.current.options 
                if self.get_square(*r).state not in [
                        State.VISITED, State.SAFE, State.BOOK, 
                    ]
            ]
            # If there have already been Filippos percepts...
            if len(self.filippos):
                # Reduce possible locations to common squares
                self.filippos = self.filippos & set(potentials)
            else:
                self.filippos = set(potentials)
            if len(self.filippos) == 1:
                self.get_square(
                    *one(self.filippos)
                ).state = State.FILIPPOS

        if Percept.BORING in percepts:
            # self.risks.update(
            #     [r for r in self.current.options if r not in self.safe]
            # )
            books = [p for p in percepts if p == Percept.BORING]
            print(f"Books: {books}")
            books_and_unknown = self.current.options.intersection(
                self.unknown.union(self.books, self.hazards)
            )
            # if len(books) == self.current.options.intersection(
            #     self.unknown.union(self.books)
            # ):
            if len(books) == len(books_and_unknown):
                print("Lengths are the same")
                for s in self.current.options:
                    square = self.get_square(*s)
                    if square.state == State.UNKNOWN:
                        square.state = State.BOOK
            else:            
                hazards_and_unknown = self.current.options.intersection(
                    self.unknown.union(self.books, self.hazards, self.filippos)
                )
                if len(percepts) == len(hazards_and_unknown):
                    print("Lengths are the same")
                    for s in self.current.options:
                        square = self.get_square(*s)
                        if square.state == State.UNKNOWN:
                            square.state = State.HAZARD

            
        # Remove known hazards as potential moves
        # for square in self.squares:
        #     square.options.difference_update(self.hazards)

    def update_probabilities(self) -> None:
        if Percept.DRONING in self.current.percepts:
            for square in self.squares:
                prob = self._square_probability(square)
                print(f"Updated {square.book_prob} probability to {prob}")
                square.book_prob = prob
                # square.book_probability = self.square_probability(square)
    
    # def square_probability(self, square: Square, prior: float = None) -> float:
    def _square_probability(self, square: Square) -> float:
        
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
        return bayes_probability(square.book_prob, specificity)


    @override
    def __str__(self):
        """Returns Grid state"""

        return (
            # f"Hazards: {self.hazards or None}\n"
            # f"Risks: {self.risks or None}\n"
            f"Filippos: {self.filippos or None}\n"
            f"Visited: {self.visited or None}\n"
            f"Safe: {self.safe or None}\n"
            f"Unknown: {self.unknown or None}\n"
            f"Hazards: {self.hazards or None}\n"
            f"Books: {self.books or None}\n"
            f"Stack: {self.stack}\n"
            # f"Route: {self.route}\n"
            f"Probabilities: {[{s.coords: s.book_prob} for s in self.squares]}\n"
        )

    # @classmethod
    # def grid(cls, size: int):
    #     """Pseudo-singleton class method for Grid"""

    #     if not cls._grid_:
    #         cls._grid_ = cls(size)
    #     return cls._grid_
