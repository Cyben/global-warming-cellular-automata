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
        self.refresh_rate = 100
        self.canvas_cells: list = [[0 for row_index in range(self.world.rows)] for col_index in range(self.world.cols)]
        self.canvas: tk.Canvas = None
        self._initiate_canvas()
        self._update_canvas()

    def mainloop(self):
        self.root.mainloop()

    def _initiate_canvas(self):
        self.root.title("Global Warming Simulation")
        self.lable = tk.Label(self.root, text="Generation {}".format(self.current_gen), font="bold")
        self.lable.pack()
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
                cell_cloud = self.canvas.create_oval((row_index + 0.13) * self.world.cell_size,
                                                     (col_index + 0.5 + 0.13) * self.world.cell_size,
                                                     (row_index + 1 - 0.13) * self.world.cell_size,
                                                     (col_index + 1 - 0.13) * self.world.cell_size,
                                                     width=0)
                self.canvas_cells[row_index][col_index] = (cell_square, cell_text, cell_cloud)
        self.root.after(self.refresh_rate, self.update_canvas_to_next_gen)

    def _update_canvas(self):
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
                    self.canvas.itemconfig(cell_cloud_id, fill="")
                elif cell_cloudness == Cloudness.CLOUDY:
                    self.canvas.itemconfig(cell_cloud_id, fill="#FFFFFF")
                elif cell_cloudness == Cloudness.RAINY:
                    self.canvas.itemconfig(cell_cloud_id, fill="#808080")

    def update_canvas_to_next_gen(self):
        if self.current_gen < self.last_gen:
            self.current_gen += 1
            self.world.update_world_to_next_gen()
            self._update_canvas()
            self.root.after(self.refresh_rate, self.update_canvas_to_next_gen)
        self.lable.config(text="Generation {}".format(self.current_gen))
