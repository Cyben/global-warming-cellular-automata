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
                 cloudness: Cloudness, air_pollution, city_pollution):
        self.row = row
        self.col = col
        self.biome_initial = biome_initial
        self.biome = Cell.biome_short[self.biome_initial]
        self.color = self._get_cell_color(biome_initial=self.biome_initial)
        self.temperature = self._get_temperature_classification(
            biome_initial=self.biome_initial)
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.cloudness = cloudness
        self.air_pollution = air_pollution
        self.city_pollution = city_pollution
        self.text = self._get_text(wind_direction=self.wind_direction, temperature=self.temperature,
                                   air_pollution=self.air_pollution)

        self.next_temperature = self.temperature
        self.next_wind_speed = self.wind_speed
        self.next_wind_direction = self.wind_direction
        self.next_cloudness = self.cloudness
        self.next_air_pollution = self.air_pollution
        self.next_biome = self.biome
        self.next_biome_initial = self.biome_initial
        self.next_color = self.color
        self.next_text = self.text

    @staticmethod
    def _get_temperature_classification(biome_initial):
        temperature_classification = {
            "L": 15,
            "S": 17,
            "I": -17,
            "F": 10,
            "C": 20,
        }

        return temperature_classification[biome_initial]

    @staticmethod
    def _get_cell_color(biome_initial):
        cell_color = {
            "L": "#8b624c",
            "S": "#006994",
            "I": "#71a6d2",
            "F": "#4a6741",
            "C": "#a0a0a0",
        }

        return cell_color[biome_initial]

    @staticmethod
    def _get_text(wind_direction: WindDirection, temperature: int, air_pollution: float):
        arrow_symbol_dict = {
            "N": "\u2191",  # unicode arrow up
            "E": "\u2192",  # unicode arrow right
            "W": "\u2190",  # unicode arrow left
            "S": "\u2193",  # unicode arrow down
        }

        arrow_direction = arrow_symbol_dict[wind_direction.value]

        cell_text = "{} {}\u2103\n P:{}%".format(arrow_direction, round(temperature, 1), round(air_pollution * 100, 1))
        return cell_text

    def _generate_next_wind_direction(self):
        random_wind_direction = random.randint(0, len(WindDirection) - 1)
        return self.wind_direction if list(WindDirection)[
                                          random_wind_direction] == self.wind_direction or \
                                      list(WindDirection)[(
                                                                  random_wind_direction + 2) % len(
                                          WindDirection)] == self.wind_direction else \
            list(WindDirection)[random_wind_direction]

    def _generate_additional_city_polution(self):
        return self.air_pollution + self.city_pollution if self.biome == "city" else self.air_pollution

    def _generate_next_air_pollution_and_cloudness(self, world: World):
        wind_speed = self.wind_speed
        neighbors_cloudness = []
        von_neumann_relative_positions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1)  # Right
        ]

        next_air_pollution = self._generate_additional_city_polution()
        for delta_row, delta_col in von_neumann_relative_positions:
            neighbor_row, neighbor_col = (self.row + delta_row) % world.rows, (self.col + delta_col) % world.cols
            neighbor_cell: Cell = world.cells[neighbor_row][neighbor_col]
            # FIXME: fix air pollution calculation, and add wind speed calculation
            if self._check_if_wind_direction_intersect(neighbor_cell_wind_direction=neighbor_cell.wind_direction, neighbor_cell_coordinates=(neighbor_row, neighbor_col)):
                next_air_pollution += neighbor_cell.air_pollution * neighbor_cell.wind_speed
                neighbors_cloudness.append(neighbor_cell.cloudness)
                wind_speed += neighbor_cell.wind_speed

        if neighbors_cloudness:
            next_cloudness = random.choice(neighbors_cloudness)
        else:
            next_cloudness = self.cloudness

        next_air_pollution -= self.air_pollution * self.wind_speed
        wind_speed -= self.wind_speed

        # normalize air_pollution
        if next_air_pollution > 1:
            next_air_pollution = 1
        if next_air_pollution < 0:
            next_air_pollution = 0

        return next_air_pollution, next_cloudness

    def _check_if_wind_direction_intersect(self, neighbor_cell_wind_direction, neighbor_cell_coordinates):
        if self.wind_direction == WindDirection.NORTH and neighbor_cell_wind_direction != WindDirection.NORTH:
            return True if self.row <= neighbor_cell_coordinates[0] else False
        if self.wind_direction == WindDirection.SOUTH and neighbor_cell_wind_direction == WindDirection.SOUTH:
            return True if self.row >= neighbor_cell_coordinates[0] else False
        if self.wind_direction == WindDirection.EAST and neighbor_cell_wind_direction == WindDirection.EAST:
            return True if self.col <= neighbor_cell_coordinates[1] else False
        if self.wind_direction == WindDirection.WEST and neighbor_cell_wind_direction == WindDirection.WEST:
            return True if self.col >= neighbor_cell_coordinates[1] else False

    def _generate_next_temperature(self, world: World):
        next_temperature = self.temperature + (world.pollution_heat_factor * self.next_air_pollution)

        if self.next_cloudness == Cloudness.RAINY:
            next_temperature -= world.rain_cold_factor
        return next_temperature

    def _generate_next_biome(self):
        new_biome_initial: str = ""
        if self.biome_initial == "I" and self.next_temperature > 0:
            new_biome_initial = "S"
        elif self.biome_initial == "S" and self.next_temperature < 0:
            new_biome_initial = "I"

        return new_biome_initial

    def generate_next_gen(self, world: World):
        self.next_wind_direction = self._generate_next_wind_direction()
        self.next_air_pollution, self.next_cloudness = self._generate_next_air_pollution_and_cloudness(world=world)
        self.next_temperature = self._generate_next_temperature(world=world)
        self.next_biome_initial = self._generate_next_biome()

    def apply_next_gen(self):
        self.wind_direction = self.next_wind_direction
        self.wind_speed = self.next_wind_speed
        self.air_pollution = self.next_air_pollution
        self.cloudness = self.next_cloudness
        self.temperature = self.next_temperature
        self.biome_initial = self.next_biome_initial if self.next_biome_initial else self.biome_initial
        self.biome = Cell.biome_short[self.biome_initial]
        self.color = self._get_cell_color(biome_initial=self.biome_initial)
        self.text = self._get_text(wind_direction=self.wind_direction, temperature=self.temperature,
                                   air_pollution=self.air_pollution)
