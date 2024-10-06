from math import sqrt
from dataclasses import dataclass
from random import randint
from typing import Literal


@dataclass
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

    if isinstance(color, str) and color in color_map:
        return color_map[color]

    return color


def pick_random_color():
    return pick_color(RGB(r=randint(0, 255), g=randint(0, 255), b=randint(0, 255)))


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
    angle: float
    speed: float
    intensity: float
    _direction: Vector = Vector(0, 0, 0)


@dataclass
class Rotation:
    direction: Literal["left", "right"]
    speed: float
    axis: Literal["x", "y", "z"]
    angle: float


@dataclass
class PlanetConfig:
    name: str
    radius: int
    position: Vector
    level_of_detail: Literal[1, 2, 3, 4]
    terrains: list[Terrain]
    color_mode: Literal["solid", "change"]
    lighting: Lighting
    rotation: Rotation
