from pygame import image, sprite, Surface
from pygame.locals import RLEACCEL


class Player(sprite.Sprite):

    def __init__(self, file, screen) -> None:
        super().__init__()
        self.surface = image.load(file).convert_alpha()
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.screen: Surface = screen

    def move(self, x: float, y: float) -> None:
        self.rect.move_ip(x, y)
        self.screen.blit(self.surface, self.rect)
