import sys

from game.grid import Grid
from game.objects import Actor
from game.util import is_quit
import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
SKY = (135, 206, 250)


def play(items_map: dict[tuple[int, int], str]):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    # screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE | pygame.DOUBLEBUF)

    # items = {k: Item(v, screen) for (k, v) in items_map.items()}
    items = {k: Actor(v, screen) for (k, v) in items_map.items()}

    grid_left: Grid = Grid(screen, 4, 70, 80, 150, WHITE, BLACK, items)
    grid_right = Grid(screen, 4, 70, 450, 150, WHITE, BLACK)

    # player = grid_left.objects.get((0, 0))
    # all_sprites = pygame.sprite.Group()
    # all_sprites.add(player)

    screen.fill(SKY)

    grid_left.draw()
    grid_right.draw()

    while True:
        for event in pygame.event.get():
            if is_quit(event):
                sys.exit()
            # elif event.type == pygame.KEYDOWN:
            #     player.move(screen, 50, 50)

        # pressed_keys = pygame.key.get_pressed()
        # player.update(screen, pressed_keys)
        # pygame.display.update()
        # clock.tick(60)


        pressed_keys = pygame.key.get_pressed()
        grid_left.update(pressed_keys)
        # player.update(screen, pressed_keys)
        # grid_left.update(screen, pressed_keys)

        #
        # for obj in all_sprites:
        #     screen.blit(obj.surface, obj.rect)

        pygame.display.flip()
        # pygame.display.update()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    play()
