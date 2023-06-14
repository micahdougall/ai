from view.objects import Actor

from dataclasses import dataclass, field
from pygame import draw, Rect, sprite, Surface
from pygame.locals import K_UP


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
    # sprites: sprite.Group = sprite.Group()
    current_square: list[int, int] = field(init=False)

    def __post_init__(self):
        self.player = self.objects.get((0, 0))
        # print(type(self.player))
        self.current_square = [self.left_margin, self.top_margin]

    def draw(self) -> None:
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.square(
                    self.left_margin + (i * self.square_size),
                    self.top_margin + (j * self.square_size),
                    self.objects.get((j, i))
                    # self.objects.get((j, i)) if not (j, i) == (0, 0) else None
                )
        # self.player.move(self.screen, 10, 10)
        # if self.player:
        #     self.sprites.add(self.player)

    def square(self, x: int, y: int, item: Actor = None) -> None:
        print(f"Draw: {x} - {y}")
        rect = Rect(x, y, self.square_size, self.square_size)
        draw.rect(self.screen, self.fill_color, rect)
        draw.rect(self.screen, self.border_color, rect, 1)
        if item:
            self.add_obj(
                item,
                x + (self.square_size / 2) - (item.surface.get_width() / 2),
                y + (self.square_size / 2) - (item.surface.get_height() / 2)
            )

    def update(self, pressed_keys):
        # print(pressed_keys)
        if pressed_keys[K_UP]:
            self.move_player()

    def add_obj(self, item: Actor, x: float, y: float):
        item.rect = item.rect.move(x, y)
        self.screen.blit(item.surface, item.rect)
        # self.screen.blit(item.surface, item.rect)

    def move_player(self):
        print("Moved")
        self.player.move(self.square_size, 0)
        self.square(*self.current_square)
        self.current_square[0] += self.square_size
        # print(self.current_square)
        # self.screen.blit(self.player.surface, self.player.rect)

