from src.universe import Planet, DistantStar

from src.utils import PlanetConfig, Vector, Lighting, Rotation, Terrain, Clouds, RGB, LevelOfDetail, Atmosphere

from src.config import screen_width, screen_height
from src.config import base_radius, base_position, base_lighting, base_planet_rotation
from src.config import terrains, clouds

import random


stars = [
    DistantStar(
        RGB(0, 0, 0),
        position=((random.randint(1, screen_width), random.randint(1, screen_height))),
        size=round(random.uniform(1, 2), 1),
    )
    for _ in range(50)
]


planets = [
    Planet(
        # 0
        name="Earth",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("earth"),
            terrain_lod=LevelOfDetail(1.4, 3),
            atmosphere=Atmosphere(color=RGB(150, 190, 255), density=0.3, height=1.3),
            clouds=clouds.get("earth"),
            wind_speed=0.006,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="left", speed=0.003, axis=["x", "y"]),
        ),
    ),
    Planet(
        # 1
        name="Moon",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("moon"),
            terrain_lod=LevelOfDetail(4),
            # atmosphere=Atmosphere(color=RGB(65, 70, 73), density=0.3, height=1.3),
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="right", speed=0.003, axis=["y"]),
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
            atmosphere=Atmosphere(color=RGB(214, 190, 140), density=0.4, height=1.1),
            clouds=clouds.get("mars"),
            wind_speed=0.02,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="right", speed=0.003, axis=["x", "y", "z"]),
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
            atmosphere=Atmosphere(color=RGB(132, 80, 183), density=0.3, height=1.6),
            clouds=clouds.get("eve"),
            wind_speed=0.02,
            color_mode="change",
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
            atmosphere=Atmosphere(color=RGB(127, 32, 21), density=0.15, height=1.2),
            clouds=clouds.get("doom"),
            lighting=base_lighting,
            planet_rotation=base_planet_rotation,
        ),
    ),
    Planet(
        # 5
        name="Atollo",
        config=PlanetConfig(
            radius=base_radius,
            position=base_position,
            terrains=terrains.get("atollo"),
            terrain_lod=LevelOfDetail(4, 1),
            atmosphere=Atmosphere(color=RGB(150, 190, 255), density=0.3, height=1.25),
            clouds=clouds.get("atollo"),
            wind_speed=0.003,
            color_mode="solid",
            lighting=base_lighting,
            planet_rotation=Rotation(direction="left", speed=0.003, axis=["x", "y"]),
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
# planetearth_assets = [planet_asset]

# with open("last_planet.txt", mode="w", encoding="utf-8") as f:
#     f.write(planet_asset.name)

planets = [planets[5]]


assets = dict(
    planets=planets,
    stars=stars,
)
