from game.util import is_quit
from game.grid import Grid
from game.objects import Item
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

    running = True
    while running:
        for event in pygame.event.get():
            if is_quit(event):
                running = False

        screen.fill(SKY)

        items = {k: Item(v) for (k, v) in items_map.items()}

        grid_left = Grid(screen, 4, 70, 80, 150, WHITE, BLACK, items)
        grid_right = Grid(screen, 4, 70, 450, 150, WHITE, BLACK)

        grid_left.draw()
        grid_right.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    play()
