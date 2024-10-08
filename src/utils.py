from math import sqrt
from dataclasses import dataclass, field
from random import randint
from typing import Literal
import random


@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int


def pick_color(
    color: bool | RGB | Literal["red", "green", "blue", "yellow", "magenta", "cyan", "white", "black"] = None,
) -> RGB:
    if not color:
        color = "black"
    elif color == True:
        color = "white"

    color_map = {
        "red": RGB(255, 0, 0),
        "green": RGB(0, 255, 0),
        "blue": RGB(0, 0, 255),
        "yellow": RGB(255, 255, 0),
        "magenta": RGB(255, 0, 255),
        "cyan": RGB(0, 255, 255),
        "white": RGB(255, 255, 255),
        "black": RGB(0, 0, 0),
    }

    return color_map.get(color, RGB(0, 0, 0)) if isinstance(color, str) else color

    # if isinstance(color, str) and color in color_map:
    #     return color_map[color]

    # return color


def pick_random_color():
    return pick_color(RGB(r=randint(0, 255), g=randint(0, 255), b=randint(0, 255)))


def set_time_of_day(time_of_day: Literal["day", "night", "morning", "noon", "evening", "random"] = "random") -> float:
    match time_of_day:
        case "night":
            angle_of_light = 1.5
        case "morning":
            angle_of_light = 0.5
        case "noon" | "day":
            angle_of_light = -1.5
        case "evening":
            angle_of_light = -3.5
        case _:
            angle_of_light = round(random.uniform(-4, 4), 1)

    return angle_of_light


@dataclass
class Terrain:
    name: str
    color: RGB
    threshold: float


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        length = sqrt(self.x**2 + self.y**2 + self.z**2)
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass
class Lighting:
    angle: float = 1.5
    speed: float = 0.1
    intensity: float = 1.0
    _direction: Vector = Vector(0, 0, 0)


@dataclass
class Rotation:
    direction: Literal["left", "right"] = "left"
    speed: float = 0.1
    axis: list[Literal["x", "y", "z"]] = None
    angle: float = 0.0

    def __post_init__(self):
        if not self.axis:
            self.axis = "y"
        if not isinstance(self.axis, list):
            self.axis = [self.axis]


@dataclass
class LevelOfDetail:
    frequency: int = 2
    weight: float = 0.5


@dataclass
class Clouds:
    height: int = 1.1
    color: RGB = RGB(255, 255, 255)
    alpha: int = 200  # should be normalized to float between 0 and 1 (also should be part of RGB as RGBA)
    threshold: int = 0.6
    lod: LevelOfDetail = LevelOfDetail
    rotation: Rotation = Rotation


@dataclass
class PlanetConfig:
    radius: int = 10
    position: Vector = Vector(x=10, y=10)
    terrains: list[Terrain] = None
    terrain_lod: LevelOfDetail = LevelOfDetail
    clouds: Clouds = None
    wind_speed: float = 0.01
    color_mode: Literal["solid", "change"] = "solid"
    lighting: Lighting = Lighting
    planet_rotation: Rotation = Rotation

    def __post_init__(self):
        if not self.terrains:
            self.terrains = [
                Terrain(name="water", color=RGB(21, 97, 178), threshold=0.59),
                Terrain(name="coast", color=RGB(252, 252, 159), threshold=0.6),
                Terrain(name="land", color=RGB(73, 150, 78), threshold=0.7),
                Terrain(name="mountains", color=RGB(112, 83, 65), threshold=0.8),
                Terrain(name="glacier", color=RGB(255, 255, 255), threshold=float("inf")),
            ]
