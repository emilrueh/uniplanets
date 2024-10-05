from src.utils import RGB, Light, Vector, pick_color, pick_random_color
from pygame import Surface, SRCALPHA
from math import sqrt, pi, cos, sin

from itertools import product
from typing import Literal

import opensimplex


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

    def draw(self, screen: Surface):
        self._update_light()
        self._draw_sphere(display=screen)

        if self.color_mode == "change":
            self._change_color_when_dark()

    @staticmethod
    def _gen_texture(normal_values: tuple, light_power: float):
        # Noise for terrain:
        norm_x = normal_values[0]
        norm_y = normal_values[1]
        norm_z = normal_values[2]

        terrain_value = 0.5 * opensimplex.noise3(norm_x, norm_y, norm_z)
        # terrain_value += (0.25 * opensimplex.noise3(norm_x * 4, norm_y * 4, norm_z * 4) + 1) / 2
        # terrain_value += (0.125 * opensimplex.noise3(norm_x * 8, norm_y * 8, norm_z * 8) + 1) / 2
        # terrain_value += (0.125 * opensimplex.noise3(norm_x * 16, norm_y * 16, norm_z * 16) + 1) / 2

        if terrain_value > 0.2:
            color = RGB(50, 20, 2)  # mountain (brown)
        elif terrain_value > 0:
            color = RGB(20, 100, 0)  # land (green)
        elif terrain_value > -0.02:
            color = RGB(255, 255, 128)  # coast (yellow)
        else:
            color = RGB(0, 40, 200)  # water (blue)

        # Mix the base color and terrain color based on lighting
        r = min(int(color.r * light_power), 255)
        g = min(int(color.g * light_power), 255)
        b = min(int(color.b * light_power), 255)
        a = 255

        texture = (r, g, b, a)
        return texture

    def _draw_sphere(self, display: Surface):
        radius_sq = self.radius * self.radius
        inv_radius = 1 / self.radius

        light_dir_x = -self._light.direction.x
        light_dir_y = -self._light.direction.y
        light_dir_z = -self._light.direction.z
        length = sqrt(light_dir_x**2 + light_dir_y**2 + light_dir_z**2)
        if length != 0:
            light_dir_x /= length
            light_dir_y /= length
            light_dir_z /= length

        sphere_surface = Surface((2 * self.radius, 2 * self.radius), SRCALPHA)

        for x, y in product(range(-self.radius, self.radius), repeat=2):
            if (x * x) + (y * y) <= radius_sq:
                norm_x = x * inv_radius
                norm_y = y * inv_radius
                norm_z = sqrt(max(0, 1 - (x * x + y * y) * inv_radius * inv_radius))

                light_power = max(norm_x * light_dir_x + norm_y * light_dir_y + norm_z * light_dir_z, 0) * self._light.intensity

                texture = self._gen_texture((norm_x, norm_y, norm_z), light_power)

                sphere_surface.set_at((x + self.radius, y + self.radius), texture)

        display.blit(sphere_surface, (self.position.x - self.radius, self.position.y - self.radius))

    def _update_light(self) -> Light:
        self.angle -= self.speed  # Increment angle
        if self.angle <= -2 * pi:
            self.angle += 2 * pi  # Wrap around after full circle
            self._color_was_changed = False

        # Compute light direction based on the angle
        light_direction = Vector(cos(self.angle), 0, sin(self.angle))
        self._light = Light(light_direction, 1.0)

    def _change_color_when_dark(self):
        is_dark = -4.9 < self.angle < -4.6

        if is_dark and not self._color_was_changed:
            self.color = pick_random_color()
            self._color_was_changed = True
