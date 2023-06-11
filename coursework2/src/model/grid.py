from coursework2.src.model.square import Square
from dataclasses import dataclass, field

from typing import ClassVar, Self


@dataclass
class Grid:
    grid_size: int
    squares: list[Square] = field(init=False)
    current: Square = field(init=False)
    stack: list[Square] = field(default_factory=list)
    route: list[Square] = field(default_factory=list)
    _grid_: ClassVar[Self] = None

    def __post_init__(self):
        self.squares = [
            Square(x, y, self.grid_size)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        ]
        self.current = self.get_square(0, 0)
        self.stack.append(self.current.coords)

    def move_to(self, to: Square):
        from_coords = self.current.coords
        print(f"Moving from {self.current.coords} to {to.coords}")
        # print(f"Stack before move: {self.stack}")
        # print(f"Unknown before move: {self.current.unknowns}")
        self.current.unknowns.remove(to.coords)
        print(f"Unknown coords at current will be: {self.current.unknowns}")
        self.current = to
        self.current.unknowns.remove(from_coords)
        print(f"Unknown coords at to will be: {to.unknowns}")

        self.stack.append(to.coords)
        # print(f"Stack after append: {self.stack}")
        self.route.append(to.coords)
        return to.dir_from(self.stack[-2])

    def back(self) -> str:
        current = self.stack.pop()
        previous = self.stack[-1]
        print(f"Moving from {self.current.coords} to {previous}")

        self.route.append(previous)
        self.current = self.get_square(*previous)

        # TODO: Confusing
        return self.current.dir_from(current)

    def get_square(self, x: int, y: int) -> Square | None:
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
