import random
from variables import WindDirection, Cloudness
from Cell import Cell


class World:
    def __init__(self, map_file: str = None, world_size: tuple = (10, 10), cell_size: int = 50):
        self.rows: int = world_size[0]
        self.cols: int = world_size[1]
        self.cell_size: int = cell_size
        self.map: list = self._read_map(map_file) if map_file else self._generate_random_map()

        self.pollution_heat_factor: float = 0.7
        self.rain_cold_factor: float = 0.4

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

                    map[row_index][col_index] = biome_initial
        return map

    def _generate_random_map(self):
        pass

    def _generate_cells(self):
        cells_matrix: list = [[0 for row_index in range(self.rows)] for col_index in range(self.cols)]
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                cells_matrix[row_index][col_index]: Cell = Cell(row=row_index,
                                                                col=col_index,
                                                                biome_initial=self.map[row_index][col_index],
                                                                wind_speed=0.5,
                                                                wind_direction=self._initiate_wind_direction(
                                                                    row=row_index,
                                                                    col=col_index),
                                                                cloudness=self._initial_cloud(
                                                                    row=row_index,
                                                                    col=col_index),
                                                                air_pollution=0.08,
                                                                city_pollution=0.001)
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
        for row_index in range(self.rows):
            for col_index in range(self.cols):
                self.cells[row_index][col_index].generate_next_gen(world=self)

        for row_index in range(self.rows):
            for col_index in range(self.cols):
                self.cells[row_index][col_index].apply_next_gen()
