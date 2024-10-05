import pygame as pg, math as m, random
from src.utils import RGB, Light, Vector, pick_color
from itertools import product
from typing import Literal


class Planet:
    def __init__(
        self,
        radius: int = 50,
        position: tuple = (10, 10),
        speed: float = 0.1,
        starting_angle: float = 1.5,
        color: RGB | Literal["red", "green", "blue", "yellow", "magenta", "cyan", "white", "black"] = None,
        color_mode: Literal["solid", "change"] = "solid",
    ):
        self.radius = radius
        self.position = Vector(x=position[0], y=position[1])
        self.speed = speed
        self.angle = starting_angle
        self.color = pick_color(color) if color else self._get_random_rgb()
        self.color_mode = color_mode
        #
        self._light = Light
        #
        self._color_was_changed = False

    def draw(self, screen: pg.Surface):
        self._update_rotation()
        self._draw_sphere(display=screen)

        if self.color_mode == "change":
            self._change_color_when_dark()

    def _draw_sphere(self, display: pg.Surface):
        radius_sq = self.radius * self.radius
        inv_radius = 1 / self.radius

        light_dir_x = -self._light.direction.x
        light_dir_y = -self._light.direction.y
        light_dir_z = -self._light.direction.z
        length = m.sqrt(light_dir_x**2 + light_dir_y**2 + light_dir_z**2)
        if length != 0:
            light_dir_x /= length
            light_dir_y /= length
            light_dir_z /= length

        sphere_surface = pg.Surface((2 * self.radius, 2 * self.radius), pg.SRCALPHA)

        for x, y in product(range(-self.radius, self.radius), repeat=2):
            if (x * x) + (y * y) <= radius_sq:
                norm_x = x * inv_radius
                norm_y = y * inv_radius
                norm_z = m.sqrt(max(0, 1 - (x * x + y * y) * inv_radius * inv_radius))

                light_power = max(norm_x * light_dir_x + norm_y * light_dir_y + norm_z * light_dir_z, 0) * self._light.intensity

                shaded_color = (
                    min(int(self.color.r * light_power), 255),
                    min(int(self.color.g * light_power), 255),
                    min(int(self.color.b * light_power), 255),
                    255,
                )

                sphere_surface.set_at((x + self.radius, y + self.radius), shaded_color)

        display.blit(sphere_surface, (self.position.x - self.radius, self.position.y - self.radius))

    def _update_rotation(self) -> Light:
        self.angle -= self.speed  # Increment angle
        if self.angle <= -2 * m.pi:
            self.angle += 2 * m.pi  # Wrap around after full circle
            self._color_was_changed = False

        # Compute light direction based on the angle
        light_direction = Vector(m.cos(self.angle), 0, m.sin(self.angle))
        self._light = Light(light_direction, 1.0)

    def _get_random_rgb(self):
        return pick_color(RGB(r=random.randint(0, 255), g=random.randint(0, 255), b=random.randint(0, 255)))

    def _change_color_when_dark(self):
        is_dark = -4.9 < self.angle < -4.6

        if is_dark and not self._color_was_changed:
            self.color = self._get_random_rgb()
            self._color_was_changed = True
