import time

from game.grid import Grid
from game.objects import Actor
from game.util import is_quit
from lib.cworld import CWorld
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
# class Game:
#
#     # Setup pygame display
#     items_map = {
#         world.student_pos: "pikachu_win.png",
#         **{c: "C.jpeg" for c in world.textbook_pos},
#         world.filippos_pos: "steve.png",
#         world.degree_pos: "degree.jpeg"
#     }
#     game.play(items_map)
class GridGame:
    _game_: ClassVar[Self] = None  # Used for 'singleton'

    # def __init__(self, i: int) -> None:
    def __init__(self, items: dict) -> None:
        super().__init__()
        self.items = items
        pygame.init()
        print(11)
        self.clock = pygame.time.Clock()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        print(22)
        MOVE = pygame.USEREVENT + 1
        items = {k: Actor(v, screen) for (k, v) in items.items()}

        print(33)
        # self.grid_left: Grid = Grid(screen, 4, 70, 80, 150, WHITE, BLACK, items)
        # self.grid_right = Grid(screen, 4, 70, 450, 150, WHITE, BLACK)

        screen.fill(SKY)

        print(44)
        # self.grid_left.draw()
        # self.grid_right.draw()

        running = True
        while running:
            for event in pygame.event.get():
                if is_quit(event):
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.grid_left.move_player()
                elif event.type == MOVE:
                    self.grid_left.move_player()

        pygame.display.flip()
        self.clock.tick(30)

    # pygame.quit()

    # def __int__(self, items) -> None:
    #     super().__init__()
        # self.items = items
        # pygame.init()
        # self.clock = pygame.time.Clock()
        # screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        #
        # items = {k: Actor(v, screen) for (k, v) in items.items()}
        #
        # self.grid_left: Grid = Grid(screen, 4, 70, 80, 150, WHITE, BLACK, items)
        # self.grid_right = Grid(screen, 4, 70, 450, 150, WHITE, BLACK)
        #
        # screen.fill(SKY)
        #
        # self.grid_left.draw()
        # self.grid_right.draw()
        #
        # pygame.display.flip()
        # self.clock.tick(30)

    # def end(self):
    #     pygame.quit()


    def move(self):
        pass
        # self.grid_left.move_player()

        # pygame.display.flip()
        # self.clock.tick(30)

    @classmethod
    # def get(cls, world: CWorld):
    def get(cls, world: int):
        """Pseudo-singleton class method for Grid"""

        # items_map = {
        #     world.student_pos: "pikachu_win.png",
        #     **{c: "C.jpeg" for c in world.textbook_pos},
        #     world.filippos_pos: "steve.png",
        #     world.degree_pos: "degree.jpeg"
        # }
        # cls._game_ = cls(items_map)
        if not cls._game_:
            # cls._game_
            items_map = {
                world.student_pos: "pikachu_win.png",
                **{c: "C.jpeg" for c in world.textbook_pos},
                world.filippos_pos: "steve.png",
                world.degree_pos: "degree.jpeg"
            }
            # items_map = world
            cls._game_ = cls(items_map)
            time.sleep(3)
            # cls._game_ = cls()
            # print(type(cls._game_))
        return cls._game_


    #
# def play(items_map: dict[tuple[int, int], str]):
# # def play(self):
#     pygame.init()
#     clock = pygame.time.Clock()
#     screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
#     # screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE | pygame.DOUBLEBUF)
#
#     # items = {k: Item(v, screen) for (k, v) in items_map.items()}
#     items = {k: Actor(v, screen) for (k, v) in items_map.items()}
#
#     grid_left: Grid = Grid(screen, 4, 70, 80, 150, WHITE, BLACK, items)
#     grid_right = Grid(screen, 4, 70, 450, 150, WHITE, BLACK)
#
#     # player = grid_left.objects.get((0, 0))
#     # all_sprites = pygame.sprite.Group()
#     # all_sprites.add(player)
#
#     screen.fill(SKY)
#
#     grid_left.draw()
#     grid_right.draw()
#
#     # while True:
#     #     for event in pygame.event.get():
#     #         if is_quit(event):
#     #             sys.exit()
#     #         elif event.type == pygame.KEYDOWN:
#     #             grid_left.move_player()
#     #         elif event.type == MOVE:
#     #             grid_left.move_player()
#
#         # pressed_keys = pygame.key.get_pressed()
#         # player.update(screen, pressed_keys)
#         # pygame.display.update()
#         # clock.tick(60)
#
#
#         # pressed_keys = pygame.key.get_pressed()
#         # grid_left.update(pressed_keys)
#         # player.update(screen, pressed_keys)
#         # grid_left.update(screen, pressed_keys)
#
#         #
#         # for obj in all_sprites:
#         #     screen.blit(obj.surface, obj.rect)
#
#         pygame.display.flip()
#         # pygame.display.update()
#         clock.tick(30)
#
#     pygame.quit()


if __name__ == '__main__':
    play()
