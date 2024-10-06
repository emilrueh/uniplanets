from src.universe import Planet

from src.utils import PlanetConfig, Vector, Lighting, Rotation, Terrain

from src.config import screen_width, screen_height
from src.config import base_radius, base_position, base_lod, base_lighting, base_rotation
from src.config import terrains


planet_assets = [
    Planet(
        config=PlanetConfig(
            name="Earth",
            radius=base_radius,
            position=base_position,
            level_of_detail=3,
            terrains=terrains.get("earth"),
            color_mode="solid",
            lighting=base_lighting,
            rotation=Rotation(direction="left", speed=0.01),
        ),
    ),
    Planet(
        config=PlanetConfig(
            name="Moon",
            radius=int(((screen_width + screen_height) // 4) * 0.3),
            position=Vector(x=screen_width // 3.5, y=screen_height // 2.5),
            level_of_detail=1,
            terrains=terrains.get("moon"),
            color_mode="solid",
            lighting=base_lighting,
            rotation=base_rotation,
        )
    ),
    Planet(
        config=PlanetConfig(
            name="Mars",
            radius=int(((screen_width + screen_height) // 4) * 0.05),
            position=Vector(x=screen_width // 1.2, y=screen_height // 3.5),
            level_of_detail=1,
            terrains=terrains.get("mars"),
            color_mode="solid",
            lighting=base_lighting,
            rotation=base_rotation,
        )
    ),
]
