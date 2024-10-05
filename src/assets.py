from src.universe import Planet
from src.config import screen_width, screen_height, rotation_speed, starting_angle, color_mode


earth = Planet(
    radius=int(((screen_width + screen_height) // 4) * 0.6),
    position=(screen_width // 2, screen_height // 2),
    speed=rotation_speed,
    starting_angle=starting_angle,
    color="blue",
    color_mode=color_mode,
)
