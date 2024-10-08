from src.universe import Planet

from src.utils import PlanetConfig, Vector, Lighting, Rotation, Terrain, Clouds, RGB, LevelOfDetail

from src.config import screen_width, screen_height
from src.config import base_radius, base_position, base_lighting, base_planet_rotation
from src.config import terrains, clouds

import random


planets = [
    Planet(
        # 0
        name="Earth",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("earth"),
            terrain_lod=LevelOfDetail(),
            clouds=clouds.get("earth"),
            wind_speed=0.01,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="left", speed=0.01, axis=["x", "y"]),
        ),
    ),
    Planet(
        # 1
        name="Moon",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("moon"),
            terrain_lod=LevelOfDetail(),
            clouds=None,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="left", speed=0.02, axis=["y"]),
        ),
    ),
    Planet(
        # 2
        name="Mars",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("mars"),
            terrain_lod=LevelOfDetail(),
            clouds=clouds.get("mars"),
            wind_speed=0.02,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="right", speed=0.01, axis=["x", "y", "z"]),
        ),
    ),
    Planet(
        # 3
        name="Eve",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("eve"),
            terrain_lod=LevelOfDetail(),
            clouds=clouds.get("eve"),
            wind_speed=0.03,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="right", speed=0.01, axis=["x"]),
        ),
    ),
    Planet(
        # 4
        name="Doom",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("doom"),
            terrain_lod=LevelOfDetail(4, 0.5),
            clouds=clouds.get("doom"),
            lighting=base_lighting,
            planet_rotation=base_planet_rotation,
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


# planet_asset = choose_planet()
# planet_assets = [planet_asset]

# with open("last_planet.txt", mode="w", encoding="utf-8") as f:
#     f.write(planet_asset.name)

planet_assets = [planets[4]]
