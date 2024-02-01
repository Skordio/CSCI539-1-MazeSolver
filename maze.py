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
    grid_size_x: int
    grid_size_y: int
    cells: dict[tuple[int, int], Cell]
    
    def __init__(self, grid_size_x=15, grid_size_y=12):
        self.set_grid_size(grid_size_x, grid_size_y)
        self.reset_cells()
        
    def set_grid_size(self, x, y):
        self.grid_size_x = x
        self.grid_size_y = y
        
    def reset_cells(self):
        self.cells = {(x, y): Cell(x, y) for x in range(self.grid_size_x) for y in range(self.grid_size_y)}
    
    def load_from_file(self, filename):
        with open(filename, 'rb') as maze_file:
            grid_size_x_byte = maze_file.read(1)
            grid_size_y_byte = maze_file.read(1)
            
            grid_size_x = int.from_bytes(grid_size_x_byte, "big")
            grid_size_y = int.from_bytes(grid_size_y_byte, "big")
            
            self.set_grid_size(grid_size_x, grid_size_y)
            self.reset_cells()
            
            start_cell_x_byte = maze_file.read(1)
            start_cell_y_byte = maze_file.read(1)
            
            start_cell_x = int.from_bytes(start_cell_x_byte, "big")
            start_cell_y = int.from_bytes(start_cell_y_byte, "big")
            
            
            end_cell_x_byte = maze_file.read(1)
            end_cell_y_byte = maze_file.read(1)
            
            end_cell_x = int.from_bytes(end_cell_x_byte, "big")
            end_cell_y = int.from_bytes(end_cell_y_byte, "big")
            
            x = 0
            y = 0
            while (byte := maze_file.read(1)) and y < grid_size_y:
                    
                byte_str = bin(int.from_bytes(byte, 'big'))[2:].rjust(8, '0')
                
                firstFour = byte_str[:4]
                
                self.cells[(x, y)].walls['top'] = firstFour[0] == '1'
                self.cells[(x, y)].walls['right'] = firstFour[1] == '1'
                self.cells[(x, y)].walls['bottom'] = firstFour[2] == '1'
                self.cells[(x, y)].walls['left'] = firstFour[3] == '1'
                
                lastFour = byte_str[4:]
                cell_number = int(lastFour, base=2)
                
                self.cells[(x, y)].number = cell_number if cell_number != 0 else None
                
                x += 1
                if x == grid_size_x:
                    x = 0
                if x == 0:
                    y += 1
                
            self.cells[(start_cell_x, start_cell_y)].is_start = True
            self.cells[(end_cell_x, end_cell_y)].is_end = True
            
    def save_to_file(self, filename):
        with open(filename, 'wb') as maze_file:
            maze_file.write(int(self.grid_size_x).to_bytes(1, 'big'))
            maze_file.write(int(self.grid_size_y).to_bytes(1, 'big'))
                    
            start_cell = next((cell for cell in self.cells.values() if cell.is_start), None)
            end_cell = next((cell for cell in self.cells.values() if cell.is_end), None)
            
            maze_file.write(int(start_cell.x).to_bytes(1, 'big'))
            maze_file.write(int(start_cell.y).to_bytes(1, 'big'))
            
            maze_file.write(int(end_cell.x).to_bytes(1, 'big'))
            maze_file.write(int(end_cell.y).to_bytes(1, 'big'))
            
            for y in range(self.grid_size_y):
                for x in range(self.grid_size_x):
                    cell = self.cells[(x, y)]
                    byte = ''
                    
                    if cell.walls['top']:
                        byte += '1'
                    else:
                        byte += '0'
                    if cell.walls['right']:
                        byte += '1'
                    else:
                        byte += '0'
                    if cell.walls['bottom']:
                        byte += '1'
                    else:
                        byte += '0'
                    if cell.walls['left']:
                        byte += '1'
                    else:
                        byte += '0'
                    
                    if cell.number is not None:
                        byte += bin(cell.number)[2:].rjust(4, '0')
                    else:
                        byte += '0000'
                    
                    maze_file.write(int(byte, base=2).to_bytes(1, 'big'))