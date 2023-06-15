from view.objects import Actor

from dataclasses import dataclass, field
from pygame import draw, Rect, Surface


@dataclass
class Grid:
    screen: Surface
    grid_size: int
    square_size: int
    left_margin: int
    top_margin: int
    fill_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    objects: dict[tuple[int, int], Actor] = field(default_factory=dict)
    player: Actor = field(init=False)
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

    def square(self, x: int, y: int, item: Actor = None) -> None:
        rect = Rect(x, y, self.square_size, self.square_size)
        draw.rect(self.screen, self.fill_color, rect)
        draw.rect(self.screen, self.border_color, rect, 1)
        if item:
            self.add_obj(
                item,
                x + (self.square_size / 2) - (item.surface.get_width() / 2),
                y + (self.square_size / 2) - (item.surface.get_height() / 2)
            )

    def add_obj(self, item: Actor, x: float, y: float):
        item.rect = item.rect.move(x, y)
        self.screen.blit(item.surface, item.rect)

    def move_player(self, move: tuple[float, float]):
        move_coords = tuple(x * self.square_size for x in move)
        print(move_coords)
        self.player.move(*move_coords)
        self.square(*self.current_square)
        self.current_square[0] += move_coords[0]
        self.current_square[1] += move_coords[1]
