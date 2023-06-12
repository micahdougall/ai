from pygame import event, KEYDOWN, QUIT
from pygame.locals import K_ESCAPE


def is_quit(event: event.Event):
    return event.type == QUIT or (
        event.type == KEYDOWN and event.key == K_ESCAPE
    )
