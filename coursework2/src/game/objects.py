from dataclasses import field, dataclass
from pygame import image, sprite, Surface
from pygame.locals import RLEACCEL


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

    def render(self, screen: Surface, x: float, y: float):
        screen.blit(
            self.surface,
            (x - self.surface.get_width() / 2, y - self.surface.get_height() / 2)
        )
