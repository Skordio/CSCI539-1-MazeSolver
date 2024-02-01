from enum import Enum
from typing import Literal

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': False, 'right': False, 'bottom': False, 'left': False}        
        self.is_start = False
        self.is_end = False
        self.number = None


class Maze:
    def __init__(self, grid_size_x, grid_size_y):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.cells = {(x, y): Cell(x, y) for x in range(self.grid_size_x) for y in range(self.grid_size_y)}