from src.universe import Planet

from src.config import earth_config


earth = Planet(config=earth_config)

# moon = Planet(
#     radius=int(((screen_width + screen_height) // 4) * 0.3),
#     position=(screen_width // 3.5, screen_height // 2.5),
#     level_of_detail=1,
#     terrains=terrains.get("moon"),
#     color_mode=color_mode,
#     starting_angle=starting_angle,
#     lighting_speed=0.01,
#     rotation_speed=0.1,
#     rotation_direction="right",
# )

# mars = Planet(
#     radius=int(((screen_width + screen_height) // 4) * 0.05),
#     position=(screen_width // 1.2, screen_height // 4),
#     level_of_detail=1,
#     terrains=terrains.get("mars"),
#     color_mode=color_mode,
#     starting_angle=starting_angle,
#     lighting_speed=0.01,
#     rotation_speed=0.1,
#     rotation_direction="right",
# )
