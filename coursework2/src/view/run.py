import time

from view.grid import Grid
from view.objects import Actor
from view.util import is_quit
# from controller.cworld import CWorld
import pygame

import sys
from typing import ClassVar, Self

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

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)


def is_quit(event: pygame.event.Event):
    return event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == K_ESCAPE
    )


class CGame:
    # _game_: ClassVar[Self] = None  # Used for 'singleton'

    # def __init__(self, items_map, world: CWorld):
    def __init__(self, items_map):

        # self.world = CWorld

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        items = {
            k: Actor(v, self.screen) for (k, v) in items_map.items()
        }
        self.grid_left: Grid = Grid(
            self.screen, 4, 70, 80, 150, WHITE, BLACK, items
        )
        self.grid_right = Grid(
            self.screen, 4, 70, 450, 150, WHITE, BLACK
        )
        self.screen.fill(SKY)
        self.grid_left.draw()
        # self.grid_right.draw()
        # while True:
        #     for event in pygame.event.get():
        #         if is_quit(event):
        #             sys.exit()
        # pygame.display.flip()
        # pygame.display.flip()
        # self.clock.tick(30)
        # time.sleep(10)

    def play(self, route: list[tuple[int, int]]):
        # self.world.play()
        print(f"Route: {route}")
        pygame.time.set_timer(MOVE, 1000)

        # import itertools

        iterator = iter(route)
        # print(iterator)


        last = (0, 0)
        route_has_next = True
        while route_has_next:
            # if new:
            #     print(f"Next: {new}")
            #     move = (new[0] - last[0], new[1] - last[1])
            #     print(f"Move: {move}")
            #     last = new
            #     # self.grid_left.move_player(move)
            #     # time.sleep(1)
            # else:
            #     route_has_next = None
            #     print("Making next none")
            # if move:
            #     self.grid_left.move_player(move)
            # else:
            #     route_has_next = None

            for event in pygame.event.get():

                if is_quit(event):
                    sys.exit()
                # elif event.type == pygame.KEYDOWN:
            #         self.grid_left.move_player()
                elif event.type == MOVE:
                    new = next(iterator, None)
                    if new:
                        print(f"Next: {new}")
                        move = (new[0] - last[0], new[1] - last[1])
                        print(f"Move: {move}")
                        last = new
                        self.grid_left.move_player(move)
                        # time.sleep(1)
                    else:
                        route_has_next = None
                        print("Making next none")
                    # move = next(iterator, None)
                    # print(f"Move: {move}")
                    # if move:
                    # self.grid_left.move_player(move)
                    # else:
                    #     route_has_next = None
            # # pygame.display.flip()
            # self.clock.tick(30)
        # pygame.quit()
        #     for each in route:
        #         print(each)
        #         self.grid_left.move_player()
        #         time.sleep(1)
            pygame.display.flip()
            self.clock.tick(30)
        print("No more moves")
        # pygame.quit()




    def move(self):
        # pass
        self.grid_left.move_player()

        pygame.display.flip()
        self.clock.tick(30)
        time.sleep(1)

    # @classmethod
    # # def get(cls, world: CWorld):
    # def get(cls, items_map: dict):
    #     """Pseudo-singleton class method for Grid"""
    #
    #     if not cls._game_:
    #         # items_map = {
    #         #     world.student_pos: "pikachu_win.png",
    #         #     **{c: "C.jpeg" for c in world.textbook_pos},
    #         #     world.filippos_pos: "steve.png",
    #         #     world.degree_pos: "degree.jpeg"
    #         # }
    #         cls._game_ = cls(items_map)
    #         # time.sleep(3)
    #     return cls._game_

