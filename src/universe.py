from src.utils import RGB, Terrain, Light, Vector, pick_color, pick_random_color
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
        terrains: list[Terrain] = None,
        level_of_detail: Literal[1, 2, 3, 4] = 2,
        color_mode: Literal["solid", "change"] = "solid",
        lighting_speed: float = 0.1,
        rotation_speed: float = 0.1,
        rotation_direction: Literal["left", "right"] = "left",
    ):
        # display
        self.radius = radius
        self.position = Vector(x=position[0], y=position[1])
        self.light_angle = starting_angle
        # appearance
        self.terrains = terrains if terrains else self._get_default_terrains()
        self.color_mode = color_mode
        # light
        self.lighting_speed = lighting_speed
        self._light = Light
        # rotation
        self.rotation_direction = rotation_direction
        self.rotation_speed = rotation_speed
        self.y = 0
        # level of detail
        self._lod_frequencies, self._lod_weights = self._calc_lod(level_of_detail)
        # etc
        self._color_was_changed = False

    def draw(self, screen: Surface):
        self._update_light()
        self._update_rotation()
        self._draw_sphere(display=screen)

        # if self.color_mode == "change":
        #     self._change_color_when_dark()

    # light

    def _update_light(self) -> Light:
        self.light_angle -= self.lighting_speed  # Increment angle
        if self.light_angle <= -2 * pi:
            self.light_angle += 2 * pi  # Wrap around after full circle
            self._color_was_changed = False

        # Compute light direction based on the angle
        light_direction = Vector(cos(self.light_angle), 0, sin(self.light_angle))
        self._light = Light(light_direction, 1.0)

    # def _change_color_when_dark(self):
    #     is_dark = -4.9 < self.light_angle < -4.6

    #     if is_dark and not self._color_was_changed:
    #         self.color = pick_random_color()
    #         self._color_was_changed = True

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
        if self.rotation_direction == "left":
            self.y += self.rotation_speed
        else:
            self.y -= self.rotation_speed
        # stabilize angles between [0, 2pi]
        self.y %= 2 * pi

    # texture

    def _get_default_terrains(self):
        return [
            Terrain(name="water", color=RGB(21, 97, 178), threshold=0.59),
            Terrain(name="coast", color=RGB(252, 252, 159), threshold=0.6),
            Terrain(name="land", color=RGB(73, 150, 78), threshold=0.7),
            Terrain(name="mountains", color=RGB(112, 83, 65), threshold=0.8),
            Terrain(name="glacier", color=RGB(255, 255, 255), threshold=float("inf")),
        ]

    @staticmethod
    def _calc_lod(lod: int):
        # Generate frequencies for specified level of detail
        frequencies = [2**i for i in range(1, lod + 1)]
        # Calculate initial weights
        weights = [1.0 / (2**i) for i in range(lod)]
        # Normalize weights so they sum up to 1
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        return frequencies, weights

    def _gen_texture(self, normal_values: tuple, light_power: float):
        norm_x, norm_y, norm_z = normal_values

        terrain_value = 0
        for i in range(len(self._lod_frequencies)):
            noise = opensimplex.noise3(norm_x * self._lod_frequencies[i], norm_y * self._lod_frequencies[i], norm_z * self._lod_frequencies[i])
            terrain_value += self._lod_weights[i] * noise

        # Normalize range from [-1, 1] to [0, 1]
        terrain_value = (terrain_value + 1) / 2

        # Determine color based on standardized terrain thresholds
        color = RGB(0, 0, 0)
        for terrain in self.terrains:
            if terrain_value <= terrain.threshold:
                color = terrain.color
                break

        # Mix terrain with light for final texture
        r = min(int(color.r * light_power), 255)
        g = min(int(color.g * light_power), 255)
        b = min(int(color.b * light_power), 255)
        a = 255

        texture = (r, g, b, a)
        return texture

    # main

    def _draw_sphere(self, display: Surface):
        # setup
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

        # draw every pixel onto x and y radius axis
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
