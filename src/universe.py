from src.utils import RGB, Light, Vector, pick_color, pick_random_color
from pygame import Surface, SRCALPHA
from math import sqrt, pi, cos, sin
import numpy as np

from itertools import product
from typing import Literal

import opensimplex


class Planet:
    def __init__(
        self,
        radius: int = 50,
        position: tuple = (10, 10),
        starting_angle: float = 1.5,
        color: RGB | Literal["red", "green", "blue", "yellow", "magenta", "cyan", "white", "black"] = None,
        color_mode: Literal["solid", "change"] = "solid",
        lighting_speed: float = 0.1,
        rotation_speed: float = 0.1,
    ):
        self.radius = radius
        self.position = Vector(x=position[0], y=position[1])
        self.light_angle = starting_angle
        self.color = pick_color(color) if color else self._get_random_rgb()
        self.color_mode = color_mode
        # light
        self.lighting_speed = lighting_speed
        self._light = Light
        # rotation
        self.rotation_speed = rotation_speed
        self.y = 0
        # etc
        self._color_was_changed = False

    def draw(self, screen: Surface):
        self._update_light()
        self._update_rotation()
        self._draw_sphere(display=screen)

        if self.color_mode == "change":
            self._change_color_when_dark()

    # light

    def _update_light(self) -> Light:
        self.light_angle -= self.lighting_speed  # Increment angle
        if self.light_angle <= -2 * pi:
            self.light_angle += 2 * pi  # Wrap around after full circle
            self._color_was_changed = False

        # Compute light direction based on the angle
        light_direction = Vector(cos(self.light_angle), 0, sin(self.light_angle))
        self._light = Light(light_direction, 1.0)

    def _change_color_when_dark(self):
        is_dark = -4.9 < self.light_angle < -4.6

        if is_dark and not self._color_was_changed:
            self.color = pick_random_color()
            self._color_was_changed = True

    # rotation

    def _gen_rotation_matrix(self):
        rotation_y = [
            [cos(self.y), 0, sin(self.y)],
            [0, 1, 0],
            [-sin(self.y), 0, cos(self.y)],
        ]
        return rotation_y

    def _rotate_normal(self, norm_x, norm_y, norm_z):
        rotation_matrix = self._gen_rotation_matrix()

        rotated_x = rotation_matrix[0][0] * norm_x + rotation_matrix[0][1] * norm_y + rotation_matrix[0][2] * norm_z
        rotated_y = rotation_matrix[1][0] * norm_x + rotation_matrix[1][1] * norm_y + rotation_matrix[1][2] * norm_z
        rotated_z = rotation_matrix[2][0] * norm_x + rotation_matrix[2][1] * norm_y + rotation_matrix[2][2] * norm_z

        return rotated_x, rotated_y, rotated_z

    def _update_rotation(self):
        self.y += self.rotation_speed
        # stabilize angles between [0, 2pi]
        self.y %= 2 * pi

    # texture

    @staticmethod
    def _gen_texture(normal_values: tuple, light_power: float):
        norm_x = normal_values[0]
        norm_y = normal_values[1]
        norm_z = normal_values[2]

        # terrain from noise
        terrain_value = 0.5 * opensimplex.noise3(norm_x, norm_y, norm_z)
        # terrain_value += (0.25 * opensimplex.noise3(norm_x * 4, norm_y * 4, norm_z * 4) + 1) / 2
        # terrain_value += (0.125 * opensimplex.noise3(norm_x * 8, norm_y * 8, norm_z * 8) + 1) / 2
        # terrain_value += (0.125 * opensimplex.noise3(norm_x * 16, norm_y * 16, norm_z * 16) + 1) / 2

        if terrain_value > 0.2:
            color = RGB(50, 20, 2)  # mountains (brown)
        elif terrain_value > 0:
            color = RGB(20, 100, 0)  # land (green)
        elif terrain_value > -0.02:
            color = RGB(255, 255, 128)  # coast (yellow)
        else:
            color = RGB(0, 40, 200)  # water (blue)

        # mix terrain with light for full texture
        r = min(int(color.r * light_power), 255)
        g = min(int(color.g * light_power), 255)
        b = min(int(color.b * light_power), 255)
        a = 255

        texture = (r, g, b, a)
        return texture

    # main

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
                # Calculate normals
                norm_x = x * inv_radius
                norm_y = y * inv_radius
                norm_z = sqrt(max(0, 1 - (x * x + y * y) * inv_radius * inv_radius))

                # Use normals for lighting
                light_power = max(norm_x * light_dir_x + norm_y * light_dir_y + norm_z * light_dir_z, 0) * self._light.intensity
                # Use rotated normals for texture
                rotated_x, rotated_y, rotated_z = self._rotate_normal(norm_x, norm_y, norm_z)
                texture = self._gen_texture((rotated_x, rotated_y, rotated_z), light_power)

                sphere_surface.set_at((x + self.radius, y + self.radius), texture)

        display.blit(sphere_surface, (self.position.x - self.radius, self.position.y - self.radius))
