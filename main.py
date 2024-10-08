import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame as pg
from src.config import screen_width, screen_height, fps, display_caption, background_color

from src.assets import assets


def draw_planets(planets: list, screen: pg.Surface):
    for planet in planets:
        planet.draw(screen)


def draw_stars(stars: list, brightness: int, screen: pg.Surface):
    for star in stars:
        r = min(star.color.r + brightness, 100)
        g = min(star.color.g + brightness, 100)
        b = min(star.color.b + brightness, 100)

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
    star_brightness = min(0, 10)

    # start
    try:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            # reset frame
            screen.fill((background_color.r, background_color.g, background_color.b))

            # display assets
            draw_stars(stars, star_brightness := star_brightness + 1, screen)
            draw_planets(planets, screen)

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
