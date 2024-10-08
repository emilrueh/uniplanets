"""
TODO:
- align terrain and clouds
- clean up utils default argument mess
- implement cloud and tectonic shifts
- allow x and z rotation for clouds
"""

from pygame import Surface, SRCALPHA
from math import sqrt, pi, cos, sin
import numpy as np
import opensimplex

from src.utils import RGB, Terrain, Clouds, Vector, Lighting, Rotation, LevelOfDetail, PlanetConfig
from src.utils import pick_random_color

from dataclasses import dataclass
from itertools import product
from functools import reduce

from typing import Literal, Callable


@dataclass
class DistantStar:
    color: RGB
    position: tuple[int, int]
    size: int


class Planet:
    def __init__(self, name: str, config: PlanetConfig):
        self.name = name
        # display
        self.position = config.position
        self.radius = config.radius
        # terrain
        self.terrains = config.terrains
        self.terrain_lod = config.terrain_lod
        self.color_mode = config.color_mode
        # clouds
        self.clouds = config.clouds
        self._cloud_radius = int(self.radius * self.clouds.height) if self.clouds else None
        # wind
        self.wind_speed = config.wind_speed
        # lighting
        self.lighting = config.lighting
        # rotation
        self.planet_rotation = config.planet_rotation
        # internal flags
        self._color_was_changed = False
        self._cloud_shift_increment = 0

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

    def _update_rotations(self, rotations: list[Rotation]):
        for rotation in rotations:
            if rotation.speed > 0:
                if rotation.direction == "left":
                    rotation.angle += rotation.speed
                else:
                    rotation.angle -= rotation.speed
                # stabilize angles between [0, 2pi]
                rotation.angle %= 2 * pi

    _multiply_matrices = staticmethod(lambda *matrices: matrices[0] if len(matrices) == 1 else reduce(np.dot, matrices))

    def _gen_rotation_matrix(self, rotation: Rotation) -> list[list] | None:
        axis_rotation_matrices = []
        if "x" in rotation.axis:
            axis_rotation_matrices.append(
                [
                    [1, 0, 0],
                    [0, cos(rotation.angle), -sin(rotation.angle)],
                    [0, sin(rotation.angle), cos(rotation.angle)],
                ]
            )
        if "y" in rotation.axis:
            axis_rotation_matrices.append(
                [
                    [cos(rotation.angle), 0, sin(rotation.angle)],
                    [0, 1, 0],
                    [-sin(rotation.angle), 0, cos(rotation.angle)],
                ]
            )
        if "z" in rotation.axis:
            axis_rotation_matrices.append(
                [
                    [cos(rotation.angle), -sin(rotation.angle), 0],
                    [sin(rotation.angle), cos(rotation.angle), 0],
                    [0, 0, 1],
                ]
            )
        return self._multiply_matrices(*axis_rotation_matrices) if axis_rotation_matrices else None

    def _rotate_normal(self, norm_x, norm_y, norm_z, rotation: Rotation):
        rotation_matrix = self._gen_rotation_matrix(rotation)

        rotated_x = rotation_matrix[0][0] * norm_x + rotation_matrix[0][1] * norm_y + rotation_matrix[0][2] * norm_z
        rotated_y = rotation_matrix[1][0] * norm_x + rotation_matrix[1][1] * norm_y + rotation_matrix[1][2] * norm_z
        rotated_z = rotation_matrix[2][0] * norm_x + rotation_matrix[2][1] * norm_y + rotation_matrix[2][2] * norm_z

        return rotated_x, rotated_y, rotated_z

    # texture

    def _build_terrain(self, noise_value):
        # Determine color based on standardized terrain thresholds
        for terrain in self.terrains:
            if noise_value <= terrain.threshold:
                return terrain.color, 255
        return None, None

    def _build_clouds(self, noise_value):
        # Determine if a cloud is displayed based on threshold
        if noise_value > self.clouds.threshold:
            return self.clouds.color, self.clouds.alpha
        return None, None

    @staticmethod
    def _compute_noise(normals: tuple, lod: LevelOfDetail, shift: float = 0):
        norm_x, norm_y, norm_z = normals

        return (
            opensimplex.noise3(
                (norm_x * lod.frequency) + shift,
                (norm_y * lod.frequency) + shift,
                (norm_z * lod.frequency) + shift,
            )
            * lod.weight
        )

    def _gen_texture(self, normals: tuple, lighting_power: float, lod: LevelOfDetail, gen_color: Callable, shift: float = 0):
        noise = self._compute_noise(normals, lod, shift)

        # Normalize range from [-1, 1] to [0, 1]
        noise_value = (noise + 1) / 2

        color, alpha = gen_color(noise_value)

        if color:
            # Mix color with lighting for final texture
            r = min(int(color.r * lighting_power), 255)
            g = min(int(color.g * lighting_power), 255)
            b = min(int(color.b * lighting_power), 255)

            return (r, g, b, alpha)
        else:
            return (0, 0, 0, 0)

    # main

    def _draw_sphere(self, display: Surface, radius: int, lod: LevelOfDetail, texture_func: Callable, rotation: Rotation, shift: int = 0):
        radius_sq = radius * radius
        inv_radius = 1 / radius

        lighting_dir_x = -self.lighting._direction.x
        lighting_dir_y = -self.lighting._direction.y
        lighting_dir_z = -self.lighting._direction.z
        length = sqrt(lighting_dir_x**2 + lighting_dir_y**2 + lighting_dir_z**2)
        if length != 0:
            lighting_dir_x /= length
            lighting_dir_y /= length
            lighting_dir_z /= length

        sphere_surface = Surface((2 * radius, 2 * radius), SRCALPHA)

        # draw every pixel onto x and y radius axis
        for x, y in product(range(-radius, radius), repeat=2):
            if (x * x) + (y * y) <= radius_sq:
                # Calculate normals
                norm_x = x * inv_radius
                norm_y = y * inv_radius
                norm_z = sqrt(max(0, 1 - (x * x + y * y) * inv_radius * inv_radius))

                # Use lighting direction
                lighting_power = max(norm_x * lighting_dir_x + norm_y * lighting_dir_y + norm_z * lighting_dir_z, 0) * self.lighting.intensity
                # Use rotated normals for texture
                rotated_x, rotated_y, rotated_z = self._rotate_normal(norm_x, norm_y, norm_z, rotation=rotation)

                texture = self._gen_texture(
                    normals=(rotated_x, rotated_y, rotated_z),
                    lighting_power=lighting_power,
                    shift=shift,
                    lod=lod,
                    gen_color=texture_func,
                )

                sphere_surface.set_at((x + radius, y + radius), texture)
        display.blit(sphere_surface, (self.position.x - radius, self.position.y - radius))

    def draw(self, screen: Surface):
        rotations = [self.planet_rotation]

        # Draw planet
        self._draw_sphere(
            display=screen,
            radius=self.radius,
            lod=self.terrain_lod,
            texture_func=self._build_terrain,
            rotation=self.planet_rotation,
        )

        # Draw clouds
        if self.clouds:
            self._cloud_shift_increment += self.wind_speed
            rotations.append(self.clouds.rotation)
            self._draw_sphere(
                display=screen,
                radius=self._cloud_radius,
                lod=self.clouds.lod,
                texture_func=self._build_clouds,
                rotation=self.clouds.rotation,
                shift=self._cloud_shift_increment,
            )

        self._update_lighting()
        self._update_rotations(rotations)

        if self.color_mode == "change":
            self._change_color_when_dark()
