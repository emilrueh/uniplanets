from src.universe import Planet

from src.config import screen_width, screen_height, lighting_speed, rotation_speed, starting_angle, color_mode


earth = Planet(
    radius=int(((screen_width + screen_height) // 4) * 0.6),
    position=(screen_width // 2, screen_height // 2),
    color="blue",
    color_mode=color_mode,
    starting_angle=starting_angle,
    lighting_speed=lighting_speed,
    rotation_speed=rotation_speed,
)
