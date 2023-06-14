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


class Actor(sprite.Sprite):

    def __init__(self, file, screen) -> None:
        super().__init__()
        self.surface = image.load(
            f"view/images/small/{file}"
        ).convert_alpha()
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        # self.rect = self.surface.get_rect().move(100, 10)
        self.rect = self.surface.get_rect()
        self.screen: Surface = screen
        # self.pos = se.
        # self.x: float = None
        # self.y: float = None
        # self.pos

    # def position(self, x: float, y: float):
    #     self.rect = self.rect.move(x, y)

    # def render(self) -> None:
    # def render(self, x, y) -> None:

        # self.screen.blit(
        #     self.surface,
        #     (x - self.surface.get_width() / 2, y - self.surface.get_height() / 2)
        # )
        # print(self.x)
        # print(self.y)
        # self.rect.move_ip(self.x, self.y)
        # self.screen.blit(self.surface, (self.x, self.y))
        # self.screen.blit(self.surface, x, y)
        # print(self.rect)
        # self.screen.blit(self.surface, self.rect)

    def update(self, pressed_keys):
        # print(pressed_keys)
        if pressed_keys[K_UP]:
            # print("Yup")
            self.move(10, 10)

    def move(self, x: float, y: float) -> None:
    # def move(self, x: float, y: float) -> None:

        # position = self.surface.get_rect().move(x, y)
        # screen.blit(screen, position, position)
        # screen.blit(self.surface, position)

        # self.rect.move_ip(x, y)
        # self.rect = self.rect.move(x, y)
        self.rect.move_ip(x, y)
        # self.render()
        self.screen.blit(self.surface, self.rect)

