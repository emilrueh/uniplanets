from src.universe import Planet

from src.config import (
    screen_width,
    screen_height,
    lighting_speed,
    rotation_speed,
    rotation_direction,
    starting_angle,
    level_of_detail,
    terrains,
    color_mode,
)


earth = Planet(
    radius=int(((screen_width + screen_height) // 4) * 0.6),
    position=(screen_width // 2, screen_height // 2),
    level_of_detail=level_of_detail,
    terrains=terrains.get("earth"),
    color_mode=color_mode,
    starting_angle=starting_angle,
    lighting_speed=lighting_speed,
    rotation_speed=rotation_speed,
    rotation_direction="left",
)

moon = Planet(
    radius=int(((screen_width + screen_height) // 4) * 0.3),
    position=(screen_width // 3.5, screen_height // 2.5),
    level_of_detail=1,
    terrains=terrains.get("moon"),
    color_mode=color_mode,
    starting_angle=starting_angle,
    lighting_speed=0.01,
    rotation_speed=0.1,
    rotation_direction="right",
)

mars = Planet(
    radius=int(((screen_width + screen_height) // 4) * 0.05),
    position=(screen_width // 1.2, screen_height // 4),
    level_of_detail=1,
    terrains=terrains.get("mars"),
    color_mode=color_mode,
    starting_angle=starting_angle,
    lighting_speed=0.01,
    rotation_speed=0.1,
    rotation_direction="right",
)
