from view.player import Player

from dataclasses import dataclass, field
from pygame import display, draw, Rect, Surface


VISITED = (192, 192, 192)
SAFE = (153, 255, 153)
RISKS = (255, 255, 153)
# BOOKS = (153, 204, 255)
BOOKS = (255, 153, 153)


@dataclass
class PyGrid:
    screen: Surface
    grid_size: int
    square_size: int
    left_margin: int
    top_margin: int
    fill_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    objects: dict[tuple[int, int], Player] = field(default_factory=dict)
    player: Player = field(init=False)
    current_square: list[int, int] = field(init=False)

    def __post_init__(self):
        self.player = self.objects.get((0, 0))
        self.current_square = [self.left_margin, self.top_margin]

    def draw(self) -> None:
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.square(
                    self.left_margin + (i * self.square_size),
                    self.top_margin + (j * self.square_size),
                    self.objects.get((j, i))
                )
        display.flip()

    def square(self, x: int, y: int, item: Player = None, new_item: bool = True, color: tuple = None) -> None:
        color = color or self.fill_color
        rect = Rect(x, y, self.square_size, self.square_size)
        draw.rect(self.screen, color, rect)
        draw.rect(self.screen, self.border_color, rect, 1)
        if item:
            self.add_obj(
                item,
                x + (self.square_size / 2) - (item.surface.get_width() / 2),
                y + (self.square_size / 2) - (item.surface.get_height() / 2),
                new_item
            )

    def add_obj(self, item: Player, x: float, y: float, new: bool):
        if new:
            item.rect = item.rect.move(x, y)
        self.screen.blit(item.surface, item.rect)
        display.flip()

    def move_player(self, move: tuple[float, float]):
        move_coords = tuple(x * self.square_size for x in move)
        self.player.move(*move_coords)
        self.square(*self.current_square)
        self.current_square[0] += move_coords[0]
        self.current_square[1] += move_coords[1]
        display.flip()

    def update_squares(self, state: dict[str, set]):
        self.color_squares(state.get("visited"), VISITED)
        self.color_squares(state.get("safe"), SAFE)
        self.color_squares(state.get("risks"), RISKS)
        self.color_squares(state.get("books"), BOOKS)
        display.flip()

    def color_squares(self, squares: set, color: tuple) -> None:
        for s in squares:
            obj = self.objects.get(s)
            if self.objects.get(s) == self.current_square:
                obj = self.player
            self.square(
                self.left_margin + (s[1] * self.square_size),
                self.top_margin + (s[0] * self.square_size),
                item=obj,
                new_item=False,
                color=color
            )
