from game.objects import Item

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
    objects: dict[tuple[int, int], Item] = field(default_factory=dict)

    def draw(self) -> None:
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.square(
                    self.left_margin + (i * self.square_size),
                    self.top_margin + (j * self.square_size),
                    self.objects.get((j, i))
                )

    def square(self, x: int, y: int, item: Item = None) -> None:
        rect = Rect(x, y, self.square_size, self.square_size)
        draw.rect(self.screen, self.fill_color, rect)
        draw.rect(self.screen, self.border_color, rect, 1)
        if item:
            item.render(self.screen, x + self.square_size/2, y + self.square_size/2)
