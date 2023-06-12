from dataclasses import field, dataclass
from pygame import image, sprite, Surface
from pygame.locals import RLEACCEL

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


@dataclass
class Item(sprite.Sprite):
    image: str
    surface: Surface = field(init=False)

    def __post_init__(self) -> None:
        super().__init__()
        self.surface = image.load(
            f"game/images/small/{self.image}"
        ).convert_alpha()
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()

    def render(self, screen: Surface, x: float, y: float) -> None:
        screen.blit(
            self.surface,
            (x - self.surface.get_width() / 2, y - self.surface.get_height() / 2)
        )

    def update(self, screen: Surface, pressed_keys):
        # print(pressed_keys)
        if pressed_keys[K_UP]:
            print("Yup")
            self.move(screen, 10, 10)

    def move(self, screen: Surface, x: float, y: float) -> None:
    # def move(self, x: float, y: float) -> None:

        # position = self.surface.get_rect().move(x, y)
        # screen.blit(screen, position, position)
        # screen.blit(self.surface, position)

        self.rect.move_ip(x, y)
        screen.blit(self.surface, self.rect)

