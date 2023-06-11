from coursework2.src.model.square import Square, Percept
from dataclasses import dataclass, field

from typing import ClassVar, Self


@dataclass
class Grid:
    grid_size: int
    squares: list[Square] = field(init=False)
    current: Square = field(init=False)
    stack: list[Square] = field(default_factory=list)
    route: list[Square] = field(default_factory=list)
    safe: set[Square] = field(default_factory=set)
    risks: set[Square] = field(default_factory=set)
    books: set[Square] = field(default_factory=set)
    filippos: set[Square] = field(default_factory=set)
    python_books: int = 1
    _grid_: ClassVar[Self] = None

    def __post_init__(self):
        self.squares = [
            Square(x, y, self.grid_size)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        ]
        self.current = self.get_square(0, 0)
        self.stack.append(self.current.coords)
        self.route.append(self.current.coords)

    def move_to(self, to: Square):
        from_coords = self.current.coords
        print(f"Moving from {self.current.coords} to {to.coords}")
        # print(f"Stack before move: {self.stack}")
        # print(f"Unknown before move: {self.current.unknowns}")
        self.current.unknowns.remove(to.coords)
        # print(f"Unknown coords at current will be: {self.current.unknowns}")
        self.current = to
        self.current.unknowns.remove(from_coords)
        # print(f"Unknown coords at to will be: {to.unknowns}")

        self.stack.append(to.coords)
        # print(f"Stack after append: {self.stack}")
        self.route.append(to.coords)
        self.safe.add(to.coords)
        print(f"Safe added {to.coords} to {self.safe}")
        return to.relative_to(self.stack[-2])

    def back(self) -> str:
        current = self.stack.pop()
        previous = self.stack[-1]
        print(f"Moving from {self.current.coords} to {previous}")

        self.route.append(previous)
        self.current = self.get_square(*previous)

        # TODO: Confusing
        return self.current.relative_to(current)

    # TODO: Refactor to single method?
    # def update_stack(self) -> None:
    #     current = self.stack.pop()
    #     previous = self.stack[-1]
    #     print(f"Moving from {self.current.coords} to {previous}")
    #
    #     self.route.append(to.coords)
    #     self.route.append(previous)
    #
    #     self.current = self.get_square(*previous)

    def is_path_explored(self) -> bool:
        """Determines whether there is an unexplored branch from a previous square"""
        # print(f"Stack is {self.stack}")
        for xy in reversed(self.stack[:-1]):
            # square = self.get_square(*xy)
            # if square.unknowns.remove(self.books):
            if self.get_square(*xy).unknowns:
                print(f"Square at {xy} not explored.")
                return False
        return True


    def safe_path(self) -> bool:
        """Determines whether there is an unexplored branch from a previous square"""
        # print(f"Stack is {self.stack}")
        for xy in reversed(self.stack[:-1]):
            unknowns = self.get_square(*xy).unknowns
            if any(u in self.safe for u in unknowns):
                print(f"Square at {xy} not explored.")
                return False
        return True

    # def shared_neighbour(self) -> :
    def update_risks(self) -> None:
        for square in self.squares:
            if len(square.percepts) == len(square.unknowns):
                self.risks.update(
                    [s for s in square.unknowns if s not in self.safe]
                )
                # TODO: Not risks or Books?
        print(f"Risks: {self.risks}")

    def update_percepts(self, percept: str) -> None:

        percepts = [Percept[p.upper()] for p in percept]
        # print(f"Percepts: {percepts}")
        self.current.percepts = percepts

        self.update_risks()

        if Percept.DRONING in percepts:
            # print(f"\033[93mCompiler noise detected, attempting to convert Filippos...", end="")
            unsafe = [r for r in self.current.options if r not in self.safe]
            # If there have already been Filippos percepts...
            if len(self.filippos):
                # Reduce possible locations to common squares
                self.filippos = self.filippos & set(unsafe)
            else:
                self.filippos = set(unsafe)
            print(f"Filippos: {self.filippos}")

        if Percept.BORING in percepts:
            printc("Yawn...C books detected in the vicinity.")
            self.risks.update(self.current.options)
                # [r for r in self.current.options if r not in self.safe]
            # )
            print(f"Risks after percept: {self.risks}")
        print(f"Safe options: {self.safe}")

    def get_square(self, x: int, y: int) -> Square | None:
        # print(f"Fetching square for x: {x} and y: {y}")
        # print(self.squares)
        return next(
            filter(lambda s: s.x == x and s.y == y, self.squares),
            None
        )

    def safe_options(self, percept) -> tuple[int, int]:
        safe_options = set()
        # print(f"Route s far: {self.route[:-1]}")
        # for xy in self.route[:-1]:
        for xy in [s for s in self.route if s != self.current.coords]:

            risks = self.current.shared_percepts(self.get_square(*xy), percept)
            # print(f"Shared risk squares with {xy} = {risks}")
            if risks:
                potential = [s for s in risks if s not in self.route]
                # print(f"Potential = {potential}")
                # if potential:
                #     print("potential exists")
                # if len(potential):
                #     print("potential has length")
                #     print(f"Detected a book at one of: {potential}.")
                for s in potential:
                    # print(f"s: {s}")
                    # print(f"type s: {type(s)}")
                    # square = self.get_square(*s)
                    # print(f"square: {square}")
                    # if "Boring" in grid.get_square(*s).percepts:
                    print(f"Book might be at {s}.")
                    # TODO: Convert this to safe list
                    # self.current.unknowns.remove(s)
                    # print(f"Self unknowns: {self.current.unknowns}")
                    # safe_option = [o for o in self.current.unknowns if not o == s]
                    safe_options.update([o for o in self.current.unknowns if not o == s])
                # TODO: Don't like this but gets rid of risk
                # return True
                print(f"Potentially safe options are: {safe_options}")
        return safe_options

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

def printc(text: str):
    print(f"\033[93m{text}\033[0m\n")
