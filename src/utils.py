from math import sqrt
from dataclasses import dataclass, field
from random import randint
from typing import Literal


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


@dataclass
class Terrain:
    name: str
    color: RGB
    threshold: float


# @dataclass
# class Clouds:
#     color: RGB
#     threshold: float = 0.5
#     height: float = 30
#     _radius: float = None


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
    axis: Literal["x", "y", "z"] = "y"
    angle: float = 0.0


class LevelOfDetail:
    def __init__(self, value: Literal[1, 2, 3, 4] = 1, frequencies: list[float] = None, weights: list[float] = None):
        self.value = value
        self.frequencies = frequencies or self._gen_frequencies()
        self.weights = weights or self._gen_weights()

    def _gen_frequencies(self):
        return [2**i for i in range(1, self.value + 1)]

    def _gen_weights(self):
        weights = [1.0 / (2**i) for i in range(self.value)]
        # normalize so they sum up to 1
        total_weight = sum(weights)
        return [w / total_weight for w in weights]


@dataclass
class Clouds:
    height: int = 1.1
    color: RGB = RGB(255, 255, 255)
    alpha: int = 200  # should be normalized to float between 0 and 1 (also should be part of RGB as RGBA)
    threshold: int = 0.6
    lod: LevelOfDetail = LevelOfDetail()


@dataclass
class PlanetConfig:
    name: str = "Earth"
    radius: int = 10
    position: Vector = Vector(x=10, y=10)
    terrains: list[Terrain] = None
    terrain_lod: LevelOfDetail = LevelOfDetail()
    clouds: Clouds = Clouds
    color_mode: Literal["solid", "change"] = "solid"
    lighting: Lighting = Lighting
    rotation: Rotation = Rotation

    def __post_init__(self):
        if not self.terrains:
            self.terrains = [
                Terrain(name="water", color=RGB(21, 97, 178), threshold=0.59),
                Terrain(name="coast", color=RGB(252, 252, 159), threshold=0.6),
                Terrain(name="land", color=RGB(73, 150, 78), threshold=0.7),
                Terrain(name="mountains", color=RGB(112, 83, 65), threshold=0.8),
                Terrain(name="glacier", color=RGB(255, 255, 255), threshold=float("inf")),
            ]
