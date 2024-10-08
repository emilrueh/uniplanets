import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg
from src.config import screen_width, screen_height, fps, display_caption, background_color

from src.assets import planet_assets


def content(screen: pg.Surface):
    for planet in planet_assets:
        planet.draw(screen)


def gameloop():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN | pg.NOFRAME | pg.SCALED)
    pg.display.set_caption(display_caption)

    fps_coll = []

    try:
        # Main loop
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            screen.fill((background_color.r, background_color.g, background_color.b))

            # display assets
            content(screen)

            # track fps average
            if (fps_get := clock.get_fps()) > 0:
                fps_coll.append(fps_get)

            # Update the display
            pg.display.flip()
            # Cap the frame rate
            clock.tick(fps)
    finally:
        if frame_count := len(fps_coll):
            print(round(sum(fps_coll) / frame_count, 2), "fps on average")
        pg.quit()


if __name__ == "__main__":
    gameloop()
