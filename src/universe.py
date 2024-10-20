from pygame import Surface, SRCALPHA, surfarray
from math import sqrt, pi, cos, sin
import numpy as np
import opensimplex

from src.utils import RGB, Terrain, Clouds, Vector, Lighting, Rotation, LevelOfDetail, PlanetConfig
from src.utils import pick_random_color

from dataclasses import dataclass
from itertools import product
from functools import reduce

from typing import Literal, Callable

from concurrent.futures import ProcessPoolExecutor


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
        # self.terrain_texture = self._generate_terrain_texture()

    # lighting

    def _update_lighting(self):
        if self.lighting.speed > 0:
            self.lighting.angle -= self.lighting.speed  # Increment angle
            if self.lighting.angle <= -2 * pi:
                self.lighting.angle += 2 * pi  # Wrap around after full circle
                self._color_was_changed = False
            self.lighting._direction = self._compute_angle_lighting_direction(self.lighting.angle)

    @staticmethod
    def _compute_angle_lighting_direction(angle) -> Vector:
        return Vector(cos(angle), 0, sin(angle))

    def _change_color_when_dark(self):
        is_dark = -4.9 < self.lighting.angle < -4.6

        if is_dark and not self._color_was_changed:
            for terrain in self.terrains:
                terrain.color = pick_random_color()

            self._color_was_changed = True

    def _get_inverted_lighting_normals(self):
        lighting_dir_x = -self.lighting._direction.x
        lighting_dir_y = -self.lighting._direction.y
        lighting_dir_z = -self.lighting._direction.z
        length = sqrt(lighting_dir_x**2 + lighting_dir_y**2 + lighting_dir_z**2)
        if length != 0:
            lighting_dir_x /= length
            lighting_dir_y /= length
            lighting_dir_z /= length

        return lighting_dir_x, lighting_dir_y, lighting_dir_z

    def _compute_lighting(self, normals: tuple, lighting_directions):
        norm_x, norm_y, norm_z = normals
        lighting_power = max(norm_x * lighting_directions[0] + norm_y * lighting_directions[1] + norm_z * lighting_directions[2], 0) * self.lighting.intensity
        return lighting_power

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

    def _rotate_normals(self, norm_x, norm_y, norm_z, rotation: Rotation):
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

    def _apply_cloud_shadows(self, terrain_surface: Surface, clouds_surface: Surface) -> Surface:
        shadow_intensity = 0.7  # Shadow multiplier to darken color (1 is fully transparent)
        shadow_strength = 3  # Scale how far shadows move with light BUG: has to be set below pi for some reason ??

        width, height = terrain_surface.get_size()

        # Get the current lighting direction
        light_dir_x = self.lighting._direction.x - 1.5
        light_dir_y = self.lighting._direction.y - 1.5 + 1

        x_shadow_offset = int(light_dir_x * shadow_strength)
        y_shadow_offset = int(light_dir_y * shadow_strength)

        for x, y in product(range(width), range(height)):
            # Apply shadow offsets to cloud position
            cloud_x = x - x_shadow_offset
            cloud_y = y - y_shadow_offset

            cloud_pixel = clouds_surface.get_at((cloud_x, cloud_y))
            if cloud_pixel.a > 0:  # There is a cloud at this location
                terrain_pixel = terrain_surface.get_at((x, y))

                # Apply shadow by darkening the terrain color
                r = int(terrain_pixel.r * shadow_intensity)
                g = int(terrain_pixel.g * shadow_intensity)
                b = int(terrain_pixel.b * shadow_intensity)

                terrain_surface.set_at((x, y), (r, g, b, terrain_pixel.a))

        return terrain_surface

    @staticmethod
    def _gen_noise(normals: tuple, lod: LevelOfDetail, shift: float = 0):
        norm_x, norm_y, norm_z = normals

        # TODO: dynamic lod: performance increase by reducing lod when unlit
        # NOTE: is it correct to implement this here tho?

        return (
            opensimplex.noise3(
                (norm_x * lod.frequency) + shift,
                (norm_y * lod.frequency) + shift,
                (norm_z * lod.frequency) + shift,
            )
            * lod.weight
        )

    def _gen_texture(self, normals: tuple, lighting_power: float, lod: LevelOfDetail, gen_color: Callable, shift: float = 0):
        noise = self._gen_noise(normals, lod, shift)

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

    def _get_normals(self, x, y, inv_radius):
        return x * inv_radius, y * inv_radius, sqrt(max(0, 1 - (x * x + y * y) * inv_radius * inv_radius))

    def _draw_sphere_texture_chunk(
        self,
        radius: int,
        radius_sq: int,
        inv_radius: float,
        lod: LevelOfDetail,
        texture_func: Callable,
        rotation: Rotation,
        shift: int,
        x_start: int,
        x_end: int,
        y_start: int,
        y_end: int,
    ):
        lighting_directions = self._get_inverted_lighting_normals()

        texture_data = {}

        for x, y in product(range(x_start, x_end), range(y_start, y_end)):
            if (x * x) + (y * y) <= radius_sq:
                norm_x, norm_y, norm_z = self._get_normals(x, y, inv_radius)
                lighting_power = self._compute_lighting((norm_x, norm_y, norm_z), lighting_directions)
                rotated_x, rotated_y, rotated_z = self._rotate_normals(norm_x, norm_y, norm_z, rotation=rotation)
                texture = self._gen_texture(
                    normals=(rotated_x, rotated_y, rotated_z),
                    lighting_power=lighting_power,
                    shift=shift,
                    lod=lod,
                    gen_color=texture_func,
                )
                texture_data[(x + radius, y + radius)] = texture

        return texture_data

    def _draw_sphere_texture_parallel(
        self,
        radius: int,
        lod: LevelOfDetail,
        texture_func: Callable,
        rotation: Rotation,
        shift: int = 0,
    ):
        num_chunks = 12  # Set number of chunks equal to the number of CPU cores
        chunk_size = int(sqrt(num_chunks))  # Calculate chunk size
        futures = []

        radius_sq = radius * radius
        inv_radius = 1 / radius

        with ProcessPoolExecutor() as executor:
            for i in range(num_chunks):
                x_start = (i % chunk_size) * (2 * radius // chunk_size) - radius
                x_end = x_start + (2 * radius // chunk_size)
                y_start = (i // chunk_size) * (2 * radius // chunk_size) - radius
                y_end = y_start + (2 * radius // chunk_size)

                futures.append(
                    executor.submit(
                        self._draw_sphere_texture_chunk,
                        radius,
                        radius_sq,
                        inv_radius,
                        lod,
                        texture_func,
                        rotation,
                        shift,
                        x_start,
                        x_end,
                        y_start,
                        y_end,
                    )
                )

            texture_data = {}
            for future in futures:
                texture_data.update(future.result())

        return texture_data

    def _gen_terrain_and_clouds_surfaces(self):
        with ProcessPoolExecutor() as executor:
            future_terrain = executor.submit(self._draw_sphere_texture_parallel, self.radius, self.terrain_lod, self._build_terrain, self.planet_rotation)

            clouds_future = None
            if self.clouds:
                self._cloud_shift_increment += self.wind_speed
                clouds_future = executor.submit(
                    self._draw_sphere_texture_parallel,
                    self._cloud_radius,
                    self.clouds.lod,
                    self._build_clouds,
                    self.clouds.rotation,
                    self._cloud_shift_increment,
                )

            # Collect results
            terrain_surface = self._process_texture_result(future_terrain, self.radius)

            clouds_surface = None
            if clouds_future:
                clouds_surface = self._process_texture_result(clouds_future, self._cloud_radius)

            # Now that both surfaces are created, apply cloud shadows to terrain
            if clouds_surface and terrain_surface:
                terrain_surface = self._apply_cloud_shadows(terrain_surface, clouds_surface)

        return terrain_surface, clouds_surface

    def _process_texture_result(self, future, radius):
        texture_data = future.result()
        surface = Surface((2 * radius, 2 * radius), SRCALPHA)

        for pos, color in texture_data.items():
            surface.set_at(pos, color)

        return surface

    def _blit_surface(self, screen, surface, x, y, radius):
        screen.blit(surface, (x - radius, y - radius))

    def draw(self, screen: Surface):
        terrain_surface, clouds_surface = self._gen_terrain_and_clouds_surfaces()

        # TODO: atmospheric affects: new sphere with gradient opacity
        # - perhaps even scattering calculated from the light direction

        self._blit_surface(screen, terrain_surface, self.position.x, self.position.y, self.radius)
        if clouds_surface:
            self._blit_surface(screen, clouds_surface, self.position.x, self.position.y, self._cloud_radius)

        # Update lighting and rotations
        self._update_lighting()
        self._update_rotations([self.planet_rotation, self.clouds.rotation])

        if self.color_mode == "change":
            self._change_color_when_dark()
