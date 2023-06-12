from player import Player
from enemy import Enemy
from cloud import Cloud

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)

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

pygame.init()
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
#
# ADDCLOUD = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDCLOUD, 1000)


player = Player()
# enemies = pygame.sprite.Group()
# clouds = pygame.sprite.Group()
# all_sprites = pygame.sprite.Group()
# all_sprites.add(player)


def is_quit(event: pygame.event.Event):
    return event.type == pygame.QUIT or (
        event.type == pygame.KEYDOWN and event.key == K_ESCAPE
    )


running = True
while running:
    for event in pygame.event.get():
        if is_quit(event):
            running = False
        # elif event.type == ADDENEMY:
        #     new_enemy = Enemy()
        #     enemies.add(new_enemy)
        #     all_sprites.add(new_enemy)
        # elif event.type == ADDCLOUD:
        #     new_cloud = Cloud()
        #     clouds.add(new_cloud)
        #     all_sprites.add(new_cloud)


    # pressed_keys = pygame.key.get_pressed()
    # player.update(pressed_keys)
    # enemies.update()
    # clouds.update()

    screen.fill((135, 206, 250))
    # screen.fill((255, 255, 255))
    # screen.fill((0, 0, 0))

    # for entity in all_sprites:
    #     screen.blit(entity.surface, entity.rect)

    # if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        # player.kill()
        # running = False

    # # Static player
    # surface = pygame.Surface((50, 50))
    # surface.fill((0, 0, 0))
    # rectangle = surface.get_rect()
    # screen.blit(player.surface, (400 - surface.get_width()/2, 300 - surface.get_height()/2))
    # screen.blit(player.surface, player.rect)

    # pygame.draw.circle(screen, (0, 0, 255), (100, 100), 25)
    gray = (200, 200, 200)
    black = (50, 50, 50)


    def draw_text(text, pos):
        img = font.render(text, True, BLACK)
        screen.blit(img, pos)

    def bordered_square(x: int, y: int, size: int, fill: tuple, border: tuple, player: Player):
        inner = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, fill, inner)
        pygame.draw.rect(screen, border, pygame.Rect(x, y, size, size), 2)
        # draw_text("Player", inner.center)
        if player:
            player.render(screen, x + size/2, y + size/2)
            # screen.blit(
            #     player.surface,
            #     (x + size/2 - player.surface.get_width()/2, y + size/2 - player.surface.get_height()/2)
                # player.rect
            # )


    def draw_grid(grid_size: int, square_size: int, left_margin: int, top_margin: int, player: Player = None, player_coords: tuple[int, int] = None):
        for i in range(grid_size):
            for j in range(grid_size):
                bordered_square(
                    left_margin + (i * square_size),
                    top_margin + (j * square_size),
                    square_size,
                    gray,
                    black,
                    player if (i, j) == player_coords else None
                )
    # char = screen.blit(player.surface, (400 - surface.get_width()/2, 300 - surface.get_height()/2))
    # print(type(player))
    # exit()
    draw_grid(4, 70, 80, 150, player, (2, 2))
    draw_grid(4, 70, 450, 150)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
