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

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


def is_quit(event: pygame.event.Event):
    return (
        event.type == pygame.QUIT
        or (
            event.type == pygame.KEYDOWN
            and event.key == K_ESCAPE
        )
    )

running = True
while running:

    for event in pygame.event.get():
        if is_quit(event):
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()


    screen.fill((135, 206, 250))
    # screen.fill((255, 255, 255))
    # screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surface, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
        player.kill()
        running = False
        
    # surface = pygame.Surface((50, 50))
    # surface.fill((0, 0, 0))
    # rectangle = surface.get_rect()
    # screen.blit(player.surface, (400 - surface.get_width()/2, 300 - surface.get_height()/2))
    screen.blit(player.surface, player.rect)


    # pygame.draw.circle(screen, (0, 0, 255), (100, 100), 25)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()