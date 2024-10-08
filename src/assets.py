from src.universe import Planet

from src.utils import PlanetConfig, Vector, Lighting, Rotation, Terrain, Clouds, RGB, LevelOfDetail

from src.config import screen_width, screen_height
from src.config import base_radius, base_position, base_planet_lod, base_lighting, base_planet_rotation
from src.config import terrains, clouds

import random


planets = [
    Planet(
        name="Earth",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("earth"),
            terrain_lod=base_planet_lod,
            clouds=clouds.get("earth"),
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="left", speed=0.01, axis=["x", "y"]),
        ),
    ),
    Planet(
        name="Moon",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("moon"),
            terrain_lod=base_planet_lod,
            clouds=None,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="left", speed=0.02, axis=["y"]),
        ),
    ),
    Planet(
        name="Mars",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("mars"),
            terrain_lod=base_planet_lod,
            clouds=clouds.get("mars"),
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="right", speed=0.01, axis=["x", "y", "z"]),
        ),
    ),
    Planet(
        name="Eve",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("eve"),
            terrain_lod=base_planet_lod,
            clouds=clouds.get("eve"),
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="right", speed=0.01, axis=["x"]),
        ),
    ),
]


def choose_planet():
    planet_asset = random.choice(planets)

    with open("last_planet.txt", mode="r", encoding="utf-8") as f:
        same_planet = f.read().strip() == planet_asset.name
        if same_planet:
            choose_planet()

    return planet_asset


planet_asset = choose_planet()
planet_assets = [planet_asset]

with open("last_planet.txt", mode="w", encoding="utf-8") as f:
    f.write(planet_asset.name)
