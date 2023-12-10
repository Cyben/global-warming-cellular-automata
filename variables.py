from enum import Enum


class WindDirection(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

class Cloudness(Enum):
    CLEAR = "clean",
    CLOUDY = "cloudy",
    RAINY = "rainy"