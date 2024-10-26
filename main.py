import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg
from src.config import screen_width, screen_height, fps, display_caption, background_color

from src.assets import assets

# from random import randint


def draw_planets(planets: list, screen: pg.Surface):
    for planet in planets:
        planet.draw(screen)


def draw_stars(stars: list, brightness: int, screen: pg.Surface):
    for star in stars:
        r = star.color.r
        g = star.color.g
        b = star.color.b

        # # TODO: flickering stars
        # # - every channel needs to have the same brightness so every star flickers white
        # random_brightness = brightness + randint(-10, 10)
        # r, g, b = [min(abs(channel + random_brightness), 100) for channel in [r, g, b]]

        r, g, b = [min(abs(channel + brightness), 100) for channel in [r, g, b]]

        pg.draw.circle(
            screen,
            (r, g, b),
            star.position,
            star.size,
        )


def gameloop():
    # setup
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN | pg.NOFRAME | pg.SCALED)
    pg.display.set_caption(display_caption)

    # assets
    planets = assets.get("planets")
    stars = assets.get("stars")

    # tracking
    fps_coll = []
    star_brightness = 0

    # start
    try:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            # reset frame
            screen.fill((background_color.r, background_color.g, background_color.b))

            # ---
            # display assets:

            if screen_width > 200:
                draw_stars(stars, star_brightness := star_brightness + 1, screen)

            draw_planets(planets, screen)

            # ---

            # update screen
            pg.display.flip()
            # cap frame rate
            clock.tick(fps)
            # track fps average
            if (fps_get := clock.get_fps()) > 0:
                fps_coll.append(fps_get)
    finally:
        if frame_count := len(fps_coll):
            print(round(sum(fps_coll) / frame_count, 2), "fps on average")
        pg.quit()


if __name__ == "__main__":
    gameloop()
