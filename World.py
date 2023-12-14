import random
import statistics
from variables import WindDirection, Cloudness
from Cell import Cell


class World:
    def __init__(self, map_file: str = None, world_size: tuple = (10, 10), cell_size: int = 50,
                 pollution_heat_factor=0.7, rain_temperature_factor=0.4, city_pollution=0.01,
                 land_initial_temperature=15, sea_initial_temperature=17, iceberg_initial_temperature=-17,
                 forest_initial_temperature=10, city_initial_temperature=20):
        self.rows: int = world_size[0]
        self.cols: int = world_size[1]
        self.cell_size: int = cell_size
        self.map: list = self._read_map(map_file) if map_file else self._generate_random_map()

        self.pollution_heat_factor: float = pollution_heat_factor
        self.rain_temperature_factor: float = rain_temperature_factor
        self.city_pollution: float = city_pollution
        self.temperature_classification = {
            "L": land_initial_temperature,
            "S": sea_initial_temperature,
            "I": iceberg_initial_temperature,
            "F": forest_initial_temperature,
            "C": city_initial_temperature,
        }

        self.avg_temp: float = 0
        self.avg_poll: float = 0
        self.land_temp: dict = {"avg": 0, "pstdev": 0}
        self.sea_temp: dict = {"avg": 0, "pstdev": 0}
        self.iceberg_temp: dict = {"avg": 0, "pstdev": 0}
        self.forest_temp: dict = {"avg": 0, "pstdev": 0}
        self.city_temp: dict = {"avg": 0, "pstdev": 0}
        self.statistics_by_biome = {"L": {"avg": 0, "pstdev": 0}, "S": {"avg": 0, "pstdev": 0},
                                    "I": {"avg": 0, "pstdev": 0},
                                    "F": {"avg": 0, "pstdev": 0}, "C": {"avg": 0, "pstdev": 0}}

        self.cells = self._generate_cells()

    def _read_map(self, map_file: str) -> list:
        with open(map_file, 'r') as file:
            self.cols = len(file.readline().strip())

        with open(map_file, 'r') as file:
            self.rows = len(file.readlines())

        map: list = [[0 for row_index in range(self.rows)] for col_index in range(self.cols)]

        with open(map_file, 'r') as file:
            for row_index in range(self.rows):
                for col_index in range(self.cols):

                    biome_initial = file.read(1)

                    if biome_initial == '\n':
                        biome_initial = file.read(1)

                    if biome_initial not in Cell.biome_short.keys():
                        print("There was a problem with the map you have provided.")
                        exit()

                    map[col_index][row_index] = biome_initial
        return map

    def _generate_random_map(self):
        pass

    def _generate_cells(self):
        temperature_list = []
        air_pollution_list = []
        cells_matrix: list = [[0 for row_index in range(self.rows)] for col_index in range(self.cols)]
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                wind_direction = self._initiate_wind_direction(
                    row=row_index,
                    col=col_index)
                cell: Cell = Cell(row=row_index,
                                  col=col_index,
                                  biome_initial=self.map[row_index][col_index],
                                  wind_speed=0.5,
                                  wind_direction=wind_direction,
                                  cloudness=self._initial_cloud(
                                      row=row_index,
                                      col=col_index),
                                  air_pollution=0.08,
                                  temperature=self.temperature_classification[self.map[row_index][col_index]],
                                  color=self._get_cell_color(self.map[row_index][col_index]),
                                  text=self._get_text(wind_direction=wind_direction,
                                                      temperature=self.temperature_classification[
                                                          self.map[row_index][col_index]],
                                                      air_pollution=0.08))
                cells_matrix[row_index][col_index] = cell
                temperature_list.append(cell.temperature)
                air_pollution_list.append(cell.air_pollution)

        self.avg_temp = statistics.mean(temperature_list)
        self.avg_poll = statistics.mean(air_pollution_list)
        return cells_matrix

    @staticmethod
    def _initiate_wind_direction(row, col):
        return random.choice(list(WindDirection))

    @staticmethod
    def _initial_cloud(row, col) -> Cloudness:
        nth_cell = 8  # create cloud for each n-th cell
        if (row + col) % nth_cell == 0:
            if (row + col) % (nth_cell * 3) == 0:
                return Cloudness.RAINY
            return Cloudness.CLOUDY
        else:
            return Cloudness.CLEAR

    def update_world_to_next_gen(self):
        temperature_list = []
        air_pollution_list = []
        temperature_list_by_biome = {"L": [], "S": [], "I": [], "F": [], "C": []}

        for row_index in range(self.rows):
            for col_index in range(self.cols):
                self.generate_next_gen(cell=self.cells[row_index][col_index])

        for row_index in range(self.rows):
            for col_index in range(self.cols):
                self.apply_next_gen(cell=self.cells[row_index][col_index])
                temperature_list.append(self.cells[row_index][col_index].temperature)
                air_pollution_list.append(self.cells[row_index][col_index].air_pollution)
                temperature_list_by_biome[self.cells[row_index][col_index].biome_initial] += [
                    self.cells[row_index][col_index].temperature]

        self._update_statistics_of_biomes(temperature_list_by_biome=temperature_list_by_biome)
        self.avg_temp = statistics.mean(temperature_list)
        self.avg_poll = statistics.mean(air_pollution_list)

    def _generate_next_gen_wind_direction(self, cell: Cell):
        random_wind_direction = random.randint(0, len(WindDirection) - 1)
        return cell.wind_direction if list(WindDirection)[
                                          random_wind_direction] == cell.wind_direction or \
                                      list(WindDirection)[(
                                                                  random_wind_direction + 2) % len(
                                          WindDirection)] == cell.wind_direction else \
            list(WindDirection)[random_wind_direction]

    def _generate_additional_city_polution_in_cell(self, cell: Cell):
        return cell.air_pollution + self.city_pollution if cell.biome == "city" else cell.air_pollution

    def _generate_next_gen_air_pollution_and_cloudness_and_wind_speed(self, cell: Cell):
        next_wind_speed = 0
        neighbors_wind_speed = []
        neighbors_cloudness = []
        von_neumann_relative_positions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1)  # Right
        ]

        next_air_pollution = self._generate_additional_city_polution_in_cell(cell)
        for delta_row, delta_col in von_neumann_relative_positions:
            neighbor_row, neighbor_col = (cell.row + delta_row) % self.rows, (cell.col + delta_col) % self.cols
            neighbor_cell: Cell = self.cells[neighbor_row][neighbor_col]
            if self._check_wind_intersect_between_cells(first_cell=cell, second_cell=neighbor_cell):
                next_air_pollution += neighbor_cell.air_pollution * neighbor_cell.wind_speed
                neighbors_cloudness.append(neighbor_cell.cloudness)
                neighbors_wind_speed.append(neighbor_cell.wind_speed)

        if neighbors_cloudness:
            next_cloudness = random.choice(neighbors_cloudness)
        else:
            next_cloudness = cell.cloudness

        next_air_pollution -= cell.air_pollution * cell.wind_speed

        # normalize air_pollution
        if next_air_pollution > 1:
            next_air_pollution = 1
        if next_air_pollution < 0:
            next_air_pollution = 0

        if neighbors_cloudness:
            next_wind_speed = sum(neighbors_wind_speed) / len(neighbors_wind_speed)
        else:
            next_wind_speed -= cell.wind_speed

        return next_air_pollution, next_cloudness, next_wind_speed

    def _check_wind_intersect_between_cells(self, first_cell: Cell, second_cell: Cell):
        if first_cell.wind_direction == WindDirection.NORTH and second_cell.wind_direction != WindDirection.NORTH:
            return True if first_cell.row <= second_cell.row else False
        if first_cell.wind_direction == WindDirection.SOUTH and second_cell.wind_direction == WindDirection.SOUTH:
            return True if first_cell.row >= second_cell.row else False
        if first_cell.wind_direction == WindDirection.EAST and second_cell.wind_direction == WindDirection.EAST:
            return True if first_cell.col <= second_cell.col else False
        if first_cell.wind_direction == WindDirection.WEST and second_cell.wind_direction == WindDirection.WEST:
            return True if first_cell.col >= second_cell.col else False

    def _generate_next_temperature(self, cell: Cell):
        next_temperature = cell.temperature + (self.pollution_heat_factor * cell.next_air_pollution)

        if cell.next_cloudness == Cloudness.RAINY:
            next_temperature -= self.rain_temperature_factor
        return next_temperature

    def _generate_next_biome(self, cell: Cell):
        new_biome_initial: str = ""
        if cell.biome_initial == "I" and cell.next_temperature > 0:
            new_biome_initial = "S"
        elif cell.biome_initial == "S" and cell.next_temperature < 0:
            new_biome_initial = "I"

        return new_biome_initial

    def generate_next_gen(self, cell: Cell):
        cell.next_wind_direction = self._generate_next_gen_wind_direction(cell=cell)
        cell.next_air_pollution, cell.next_cloudness, cell.next_wind_speed = self._generate_next_gen_air_pollution_and_cloudness_and_wind_speed(
            cell=cell)
        cell.next_temperature = self._generate_next_temperature(cell=cell)
        cell.next_biome_initial = self._generate_next_biome(cell=cell)

    def apply_next_gen(self, cell: Cell):
        cell.wind_direction = cell.next_wind_direction
        cell.wind_speed = cell.next_wind_speed
        cell.air_pollution = cell.next_air_pollution
        cell.cloudness = cell.next_cloudness
        cell.temperature = cell.next_temperature
        cell.biome_initial = cell.next_biome_initial if cell.next_biome_initial else cell.biome_initial
        cell.biome = Cell.biome_short[cell.biome_initial]
        cell.color = self._get_cell_color(biome_initial=cell.biome_initial)
        cell.text = self._get_text(wind_direction=cell.wind_direction, temperature=cell.temperature,
                                   air_pollution=cell.air_pollution)

    def _update_statistics_of_biomes(self, temperature_list_by_biome: dict):
        for biome_initial, temperature_list in temperature_list_by_biome.items():
            self.statistics_by_biome[biome_initial]["avg"] = round(statistics.mean(temperature_list), 2)
            self.statistics_by_biome[biome_initial]["pstdev"] = round(statistics.pstdev(temperature_list), 2)

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

        cell_text = f"{arrow_direction} {round(temperature, 1)}\u2103\n P:{round(air_pollution * 100, 1)}%"
        return cell_text
