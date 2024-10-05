import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg
from src.config import screen_width, screen_height, fps, display_caption, background_color

from src.assets import earth


def content(screen: pg.Surface):
    earth.draw(screen)


def gameloop():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN | pg.NOFRAME | pg.SCALED)
    pg.display.set_caption(display_caption)
    screen.fill((background_color.r, background_color.g, background_color.b))

    try:
        # Main loop
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            content(screen)

            # Update the display
            pg.display.flip()
            # Cap the frame rate
            clock.tick(fps)
    finally:
        pg.quit()


if __name__ == "__main__":
    gameloop()
