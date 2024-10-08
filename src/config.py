from src.utils import pick_color, RGB, Terrain, Clouds, Lighting, Rotation, Vector, LevelOfDetail, set_time_of_day
from typing import Literal
import random


# display settings
resolution, upscale = "1920x1080", 0.1
fps = 30

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "UniPlanets"
background_color = pick_color("black")

# planet settings

angle_of_light = set_time_of_day("day")

base_lighting = Lighting(angle=angle_of_light, speed=0.01, intensity=1.0)
base_planet_rotation = Rotation(direction="left", speed=0.01, axis="y", angle=0.0)
base_radius = int(((screen_width + screen_height) // 4) * 0.6)
base_position = Vector(x=screen_width // 2, y=screen_height // 2)

terrains = {
    "earth": [
        Terrain(name="deep_water", color=RGB(50, 112, 211), threshold=0.55),
        # Terrain(name="shallow_water", color=RGB(100, 152, 234), threshold=0.6),
        # Terrain(name="coast", color=RGB(238, 232, 169), threshold=0.62),
        # Terrain(name="land", color=RGB(140, 185, 122), threshold=0.7),
        Terrain(name="forest", color=RGB(84, 161, 109), threshold=float("inf")),
    ],
    "moon": [
        Terrain(name="dust", color=RGB(65, 70, 73), threshold=0.4),
        Terrain(name="rim", color=RGB(45, 48, 51), threshold=0.7),
        Terrain(name="crater", color=RGB(32, 34, 35), threshold=float("inf")),
    ],
    "mars": [
        Terrain(name="desert", color=RGB(160, 80, 43), threshold=0.58),
        Terrain(name="mountain", color=RGB(214, 133, 83), threshold=float("inf")),
    ],
    "eve": [
        Terrain(name="sea", color=RGB(132, 80, 183), threshold=0.6),
        Terrain(name="land", color=RGB(212, 80, 165), threshold=float("inf")),  # last terrain (highest) needs rest of the scale
    ],
    "doom": [
        Terrain(name="soil", color=RGB(30, 28, 28), threshold=0.5),
        Terrain(name="lava", color=RGB(127, 32, 21), threshold=0.56),
        Terrain(name="magma", color=RGB(244, 165, 61), threshold=float("inf")),
    ],
}

clouds = {
    "earth": Clouds(
        height=1.1,
        color=RGB(255, 255, 255),
        alpha=150,
        threshold=0.6,
        lod=LevelOfDetail(4, 1),
        rotation=Rotation(direction="left", speed=0.01, axis=["y", "z"]),
    ),
    "mars": Clouds(
        height=1.2,
        color=RGB(255, 220, 160),
        alpha=130,
        threshold=0.68,
        lod=LevelOfDetail(),
        rotation=Rotation(direction="right", speed=0.005, axis=["y", "z"]),
    ),
    "eve": Clouds(
        height=1.15,
        color=RGB(150, 150, 255),
        alpha=100,
        threshold=0.5,
        lod=LevelOfDetail(),
        rotation=Rotation(direction="left", speed=0.01, axis=["x", "z"]),
    ),
    "doom": Clouds(
        height=1.2,
        color=RGB(100, 100, 100),
        alpha=100,
        threshold=0.45,
        lod=LevelOfDetail(),
        rotation=Rotation(direction="right", speed=0.01, axis="y"),
    ),
}
