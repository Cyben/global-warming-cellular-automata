import tkinter as tk
from World import World
from Cell import Cell
from variables import WindDirection, Cloudness


class Simulation:
    def __init__(self, world: World, last_gen: int = 365):
        self.world: World = world
        self.last_gen: int = last_gen
        self.current_gen = 1
        self.root: tk.Tk = tk.Tk()
        self.refresh_rate = 50
        self.canvas_cells: list = [[0 for row_index in range(self.world.rows)] for col_index in range(self.world.cols)]
        self.canvas: tk.Canvas = None
        self._initiate_canvas()
        self._update_canvas()

    def mainloop(self):
        self.root.mainloop()

    def _initiate_canvas(self):
        self.root.title("Global Warming Simulation")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.configure(bg="lightblue")
        self.gen_lable = tk.Label(self.root, text=f"Global Warming Simulation\nGeneration {self.current_gen}",
                                  font="bold", height=2, bg="lightblue")
        self.gen_lable.pack(side="top")
        self.temp_and_poll_label = tk.Label(self.root,
                                            text=f"Average temperature is: {round(self.world.avg_temp, 2)}\u2103\t\tAverage pollution is: {round(self.world.avg_poll, 2)}")
        self.temp_and_poll_label.pack(side="top")
        self.land_label = tk.Label(self.root, bg="lightblue",
                                   text=f"Land   -   \t Initital temperature: {self.world.temperature_classification['L']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['L']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['L']['pstdev']}")
        self.land_label.pack(side="bottom")
        self.sea_label = tk.Label(self.root, bg="lightblue",
                                   text=f"Sea   -   \t Initital temperature: {self.world.temperature_classification['S']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['S']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['S']['pstdev']}")
        self.sea_label.pack(side="bottom")
        self.iceberg_label = tk.Label(self.root, bg="lightblue",
                                   text=f"Iceberg   -   \t Initital temperature: {self.world.temperature_classification['I']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['I']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['I']['pstdev']}")
        self.iceberg_label.pack(side="bottom")
        self.forest_label = tk.Label(self.root, bg="lightblue",
                                   text=f"Forest   -   \t Initital temperature: {self.world.temperature_classification['F']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['F']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['F']['pstdev']}")
        self.forest_label.pack(side="bottom")
        self.city_label = tk.Label(self.root, bg="lightblue",
                                   text=f"City   -   \t Initital temperature: {self.world.temperature_classification['C']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['C']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['C']['pstdev']}")
        self.city_label.pack(side="bottom")
        self.canvas = tk.Canvas(master=self.root,
                                height=self.world.rows * self.world.cell_size,
                                width=self.world.cols * self.world.cell_size)
        self.canvas.pack()
        for row_index in range(self.world.rows):
            for col_index in range(self.world.cols):
                cell_square = self.canvas.create_rectangle(row_index * self.world.cell_size,
                                                           col_index * self.world.cell_size,
                                                           (row_index + 1) * self.world.cell_size,
                                                           (col_index + 1) * self.world.cell_size)
                cell_text = self.canvas.create_text((row_index + 0.5) * self.world.cell_size,
                                                    (col_index + 0.25) * self.world.cell_size,
                                                    font=('Helvetica 8 bold'))
                cell_cloud = self._create_cloud(row_index=row_index, col_index=col_index)
                self.canvas_cells[row_index][col_index] = (cell_square, cell_text, cell_cloud)

        self.root.after(self.refresh_rate, self.update_canvas_to_next_gen)

    def _create_cloud(self, row_index, col_index):
        cell_cloud = []
        cell_cloud.append(self.canvas.create_oval((row_index + 0.13) * self.world.cell_size,
                                                  (col_index + 0.63) * self.world.cell_size,
                                                  (row_index + 0.87) * self.world.cell_size,
                                                  (col_index + 0.89) * self.world.cell_size,
                                                  width=0))
        cell_cloud.append(self.canvas.create_oval((row_index + 0.20) * self.world.cell_size,
                                                  (col_index + 0.70) * self.world.cell_size,
                                                  (row_index + 0.6) * self.world.cell_size,
                                                  (col_index + 0.6) * self.world.cell_size,
                                                  width=0))
        cell_cloud.append(self.canvas.create_oval((row_index + 0.80) * self.world.cell_size,
                                                  (col_index + 0.5 + 0.20) * self.world.cell_size,
                                                  (row_index + 1 - 0.40) * self.world.cell_size,
                                                  (col_index + 1 - 0.40) * self.world.cell_size,
                                                  width=0))

        return cell_cloud

    def _update_canvas(self):
        cloud_color = ""
        for row_index in range(self.world.rows):
            for col_index in range(self.world.cols):
                cell: Cell = self.world.cells[row_index][col_index]
                cell_color: str = cell.color
                cell_text = cell.text
                cell_cloudness: Cloudness = cell.cloudness
                (cell_square_id, cell_text_id, cell_cloud_id) = self.canvas_cells[row_index][col_index]
                self.canvas.itemconfig(cell_square_id, fill=cell_color)
                self.canvas.itemconfig(cell_text_id, text=cell_text)
                if cell_cloudness == Cloudness.CLEAR:
                    cloud_color = ""
                elif cell_cloudness == Cloudness.CLOUDY:
                    cloud_color = "#FFFFFF"
                elif cell_cloudness == Cloudness.RAINY:
                    cloud_color = "#808080"

                for object in cell_cloud_id:
                    self.canvas.itemconfig(object, fill=cloud_color)

    def update_canvas_to_next_gen(self):
        if self.current_gen < self.last_gen:
            self.current_gen += 1
            self.world.update_world_to_next_gen()
            self._update_canvas()
            self.root.after(self.refresh_rate, self.update_canvas_to_next_gen)
        self.gen_lable.config(text=f"Global Warming Simulation\nGeneration {self.current_gen}")
        self.temp_and_poll_label.config(
            text=f"""Average temperature is: {round(self.world.avg_temp, 2)} \u2103\t\tAverage pollution is: {round(self.world.avg_poll, 2)}""")
        self.land_label.config(
            text=f"Land   -   \t Initital temperature: {self.world.temperature_classification['L']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['L']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['L']['pstdev']}")
        self.sea_label.config(
            text=f"Sea   -   \t Initital temperature: {self.world.temperature_classification['S']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['S']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['S']['pstdev']}")
        self.iceberg_label.config(
            text=f"Iceberg   -   \t Initital temperature: {self.world.temperature_classification['I']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['I']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['I']['pstdev']}")
        self.forest_label.config(
            text=f"Forest   -   \t Initital temperature: {self.world.temperature_classification['F']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['F']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['F']['pstdev']}")
        self.city_label.config(
            text=f"City   -   \t Initital temperature: {self.world.temperature_classification['C']}\u2103\t\tAverage temperature: {self.world.statistics_by_biome['C']['avg']}\u2103\t\tPopulation standard deviation: {self.world.statistics_by_biome['C']['pstdev']}")