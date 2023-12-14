import random

import World
from variables import WindDirection, Cloudness


class Cell:
    biome_short = {
        "L": "land",
        "S": "sea",
        "I": "iceberg",
        "F": "forest",
        "C": "city",
    }

    def __init__(self, row: int, col: int, biome_initial: str, wind_speed: float, wind_direction: WindDirection,
                 cloudness: Cloudness, air_pollution, temperature, color, text):
        self.row = row
        self.col = col
        self.biome_initial = biome_initial
        self.biome = Cell.biome_short[self.biome_initial]
        self.color = color
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.cloudness = cloudness
        self.air_pollution = air_pollution
        self.text = text

        self.next_temperature = self.temperature
        self.next_wind_speed = self.wind_speed
        self.next_wind_direction = self.wind_direction
        self.next_cloudness = self.cloudness
        self.next_air_pollution = self.air_pollution
        self.next_biome = self.biome
        self.next_biome_initial = self.biome_initial
        self.next_color = self.color
        self.next_text = self.text