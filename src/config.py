from src.utils import pick_color, RGB, Terrain, Clouds, Lighting, Rotation, Vector, LevelOfDetail, set_time_of_day
from typing import Literal
import random


# display settings
resolution, upscale = "1920x1080", 0.1
fps = 10

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "UniPlanets"
background_color = pick_color("black")

# planet settings

angle_of_light = set_time_of_day("random")

base_lighting = Lighting(angle=angle_of_light, speed=0.01, intensity=1.0)
base_rotation = Rotation(direction="left", speed=0.01, axis="y", angle=0.0)
base_planet_lod = LevelOfDetail(1, frequencies=[2, 4, 8, 16], weights=[0.5, 0.25, 0.125, 0.125])
base_clouds_lod = LevelOfDetail(1, frequencies=[4, 8, 16, 32], weights=[0.75, 0.125, 0.0625, 0.0625])
base_radius = int(((screen_width + screen_height) // 4) * 0.6)
base_position = Vector(x=screen_width // 2, y=screen_height // 2)

terrains = {
    "earth": [
        Terrain(name="deep_water", color=RGB(50, 112, 211), threshold=0.55),
        Terrain(name="shallow_water", color=RGB(100, 152, 234), threshold=0.6),
        Terrain(name="coast", color=RGB(238, 232, 169), threshold=0.62),
        Terrain(name="land", color=RGB(140, 185, 122), threshold=0.7),
        Terrain(name="forest", color=RGB(84, 161, 109), threshold=float("inf")),
    ],
    "moon": [
        Terrain(name="dust", color=RGB(65, 70, 73), threshold=0.4),
        Terrain(name="rim", color=RGB(45, 48, 51), threshold=0.7),
        Terrain(name="crater", color=RGB(32, 34, 35), threshold=float("inf")),
    ],
    "mars": [
        Terrain(name="desert", color=RGB(160, 80, 43), threshold=0.6),
        Terrain(name="mountain", color=RGB(214, 133, 83), threshold=float("inf")),
    ],
    "eve": [
        Terrain(name="sea", color=RGB(132, 80, 183), threshold=0.6),
        Terrain(name="land", color=RGB(212, 80, 165), threshold=float("inf")),  # last terrain (highest) needs rest of the scale
    ],
}

clouds = {
    "earth": Clouds(height=1.1, color=RGB(255, 255, 255), alpha=200, threshold=0.6, lod=base_clouds_lod),
}
