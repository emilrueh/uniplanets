from src.utils import pick_color, RGB, Terrain, Clouds, Lighting, Rotation, Vector, LevelOfDetail, set_time_of_day
from typing import Literal
import random


# display settings
# resolution, upscale = "1920x1080", 0.1
resolution, upscale = "1000x1000", 0.1
fps = 30

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "UniPlanets"
background_color = pick_color("black")

# planet settings

angle_of_light = set_time_of_day("day")

base_lighting = Lighting(angle=angle_of_light, speed=0.03, intensity=1.0)
base_planet_rotation = Rotation(direction="left", speed=0.01, axis="y", angle=0.0)
base_radius = int(((screen_width + screen_height) // 4) * 0.6)
base_position = Vector(x=screen_width // 2, y=screen_height // 2)

terrains = {
    "earth": [
        Terrain(name="deep_water", color=RGB(50, 112, 211), threshold=0.5),
        Terrain(name="forest", color=RGB(84, 161, 109), threshold=float("inf")),
    ],
    "moon": [
        Terrain(name="dust", color=RGB(65, 70, 73), threshold=0.43),
        Terrain(name="rim", color=RGB(45, 48, 51), threshold=0.54),
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
    "atollo": [
        Terrain(name="deep_water", color=RGB(50, 112, 211), threshold=0.45),
        Terrain(name="shallow_water", color=RGB(100, 152, 234), threshold=0.55),
        Terrain(name="coast", color=RGB(238, 232, 169), threshold=0.6),
        Terrain(name="land", color=RGB(140, 185, 122), threshold=0.65),
        Terrain(name="forest", color=RGB(84, 161, 109), threshold=float("inf")),
    ],
}

clouds = {
    "earth": Clouds(
        height=1.03,
        color=RGB(255, 255, 255),
        alpha=240,
        threshold=0.6,
        lod=LevelOfDetail(7, 2),
        rotation=Rotation(direction="left", speed=0.001, axis=["y", "z"]),
    ),
    "mars": Clouds(
        height=1.04,
        color=RGB(255, 210, 160),
        alpha=200,
        threshold=0.6,
        lod=LevelOfDetail(4),
        rotation=Rotation(direction="right", speed=0.005, axis=["y", "z"]),
    ),
    "eve": Clouds(
        height=1.09,
        color=RGB(150, 150, 255),
        alpha=220,
        threshold=0.59,
        lod=LevelOfDetail(5),
        rotation=Rotation(direction="left", speed=0.001, axis=["x", "z"]),
    ),
    "doom": Clouds(
        height=1.06,
        color=RGB(50, 50, 50),
        alpha=255,
        threshold=0.45,
        lod=LevelOfDetail(3),
        rotation=Rotation(direction="right", speed=0.01, axis="y"),
        shadow_alpha=0.2,
    ),
    "atollo": Clouds(
        height=1.05,
        color=RGB(255, 255, 255),
        alpha=200,
        threshold=0.55,
        lod=LevelOfDetail(4.5, 0.5),
        rotation=Rotation(direction="left", speed=0.003, axis=["y", "z"]),
    ),
}
