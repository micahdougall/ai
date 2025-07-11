from view.pygrid import PyGrid
from view.player import Player

import pygame
from pygame.locals import K_ESCAPE
import sys
import time


# TODO: Review what's needed
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
MOVE = pygame.USEREVENT + 1


class CGame:
    def __init__(self, items_map):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        items = {
            k: Player(v, self.screen) for (k, v) in items_map.items()
        }
        self.grid_left: PyGrid = PyGrid(
            self.screen, 4, 70, 80, 150, WHITE, BLACK, items
        )
        self.grid_right = PyGrid(
            self.screen, 4, 70, 450, 150, WHITE, BLACK
        )
        self.screen.fill(SKY)
        self.grid_left.draw()
        pygame.display.flip()
        self.clock.tick(30)

    def play(self, states: list[dict]):
        pygame.time.set_timer(MOVE, 1000)

        iterator = iter(states)
        state = next(iterator, None)

        print(f"State: {state}")

        if state:
            self.grid_left.update_squares(state)
        route_has_next = True
        while route_has_next:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and event.key == K_ESCAPE
                ):
                    sys.exit()
                elif event.type == MOVE:
                    pygame.time.wait(1000)
                    new = next(iterator, None)
                    print(f"State: {new}")
                    if new:
                        coords = new.get("coords")
                        move = (
                            coords[1] - state.get("coords")[1],
                            coords[0] - state.get("coords")[0]
                        )
                        state = new
                        self.grid_left.update_squares(new)
                        self.grid_left.move_player(move)
                    else:
                        route_has_next = False
            pygame.display.flip()
            self.clock.tick(5)
        print("No more moves")
        time.sleep(5)
        # pygame.quit()

    def move(self):
        self.grid_left.move_player()

        pygame.display.flip()
        # self.clock.tick(30)
        # time.sleep(1)
