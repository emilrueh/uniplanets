from pygame import Surface, SRCALPHA
from math import sqrt, pi, cos, sin

from src.utils import RGB, Terrain, Vector, Lighting, Rotation, PlanetConfig
from src.utils import pick_random_color

from itertools import product
from typing import Literal

import opensimplex


class Planet:
    def __init__(self, config: PlanetConfig):
        # display
        self.position = config.position
        self.radius = config.radius
        # appearance
        self.terrains = config.terrains
        self.color_mode = config.color_mode
        # lighting
        self.lighting = config.lighting
        # rotation
        self.rotation = config.rotation
        # level of detail
        self._lod_frequencies, self._lod_weights = self._calc_lod(config.level_of_detail)
        # etc
        self._color_was_changed = False

    def draw(self, screen: Surface):
        self._update_lighting()
        self._update_rotation()
        self._draw_sphere(display=screen)

        if self.color_mode == "change":
            self._change_color_when_dark()

    # lighting

    def _update_lighting(self):
        if self.lighting.speed > 0:
            self.lighting.angle -= self.lighting.speed  # Increment angle
            if self.lighting.angle <= -2 * pi:
                self.lighting.angle += 2 * pi  # Wrap around after full circle
                self._color_was_changed = False
            self.lighting._direction = self._compute_lighting_direction(self.lighting.angle)

    @staticmethod
    def _compute_lighting_direction(angle) -> Vector:
        return Vector(cos(angle), 0, sin(angle))

    def _change_color_when_dark(self):
        is_dark = -4.9 < self.lighting.angle < -4.6

        if is_dark and not self._color_was_changed:
            for terrain in self.terrains:
                terrain.color = pick_random_color()

            self._color_was_changed = True

    # rotation

    def _update_rotation(self):
        if self.rotation.speed > 0:
            if self.rotation.direction == "left":
                self.rotation.angle += self.rotation.speed
            else:
                self.rotation.angle -= self.rotation.speed
            # stabilize angles between [0, 2pi]
            self.rotation.angle %= 2 * pi

    def _gen_rotation_matrix(self):
        if self.rotation.axis == "y":
            rotation_matrix = [
                [cos(self.rotation.angle), 0, sin(self.rotation.angle)],
                [0, 1, 0],
                [-sin(self.rotation.angle), 0, cos(self.rotation.angle)],
            ]
        else:
            raise ValueError(f"{self.rotation.axis} rotation has not been implemented yet! Choose 'y' instead.")
        return rotation_matrix

    def _rotate_normal(self, norm_x, norm_y, norm_z):
        rotation_matrix = self._gen_rotation_matrix()

        rotated_x = rotation_matrix[0][0] * norm_x + rotation_matrix[0][1] * norm_y + rotation_matrix[0][2] * norm_z
        rotated_y = rotation_matrix[1][0] * norm_x + rotation_matrix[1][1] * norm_y + rotation_matrix[1][2] * norm_z
        rotated_z = rotation_matrix[2][0] * norm_x + rotation_matrix[2][1] * norm_y + rotation_matrix[2][2] * norm_z

        return rotated_x, rotated_y, rotated_z

    # texture

    @staticmethod
    def _get_default_terrains():
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

    def _gen_texture(self, normal_values: tuple, lighting_power: float):
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

        # Mix terrain with lighting for final texture
        r = min(int(color.r * lighting_power), 255)
        g = min(int(color.g * lighting_power), 255)
        b = min(int(color.b * lighting_power), 255)
        a = 255

        texture = (r, g, b, a)
        return texture

    # main

    def _draw_sphere(self, display: Surface):
        # setup
        radius_sq = self.radius * self.radius
        inv_radius = 1 / self.radius

        lighting_dir_x = -self.lighting._direction.x
        lighting_dir_y = -self.lighting._direction.y
        lighting_dir_z = -self.lighting._direction.z
        length = sqrt(lighting_dir_x**2 + lighting_dir_y**2 + lighting_dir_z**2)
        if length != 0:
            lighting_dir_x /= length
            lighting_dir_y /= length
            lighting_dir_z /= length

        sphere_surface = Surface((2 * self.radius, 2 * self.radius), SRCALPHA)

        # draw every pixel onto x and y radius axis
        for x, y in product(range(-self.radius, self.radius), repeat=2):
            if (x * x) + (y * y) <= radius_sq:
                # Calculate normals
                norm_x = x * inv_radius
                norm_y = y * inv_radius
                norm_z = sqrt(max(0, 1 - (x * x + y * y) * inv_radius * inv_radius))

                # Use normals for lighting
                lighting_power = max(norm_x * lighting_dir_x + norm_y * lighting_dir_y + norm_z * lighting_dir_z, 0) * self.lighting.intensity
                # Use rotated normals for texture
                rotated_x, rotated_y, rotated_z = self._rotate_normal(norm_x, norm_y, norm_z)
                texture = self._gen_texture((rotated_x, rotated_y, rotated_z), lighting_power)

                sphere_surface.set_at((x + self.radius, y + self.radius), texture)

        display.blit(sphere_surface, (self.position.x - self.radius, self.position.y - self.radius))
