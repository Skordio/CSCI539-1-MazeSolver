from enum import Enum
from typing import Literal, List, Dict, Tuple

class Solution:
    path: list[tuple[int, int]]

    def __init__(self):
        self.path = []

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': False, 'right': False, 'bottom': False, 'left': False}        
        self.is_start = False
        self.is_end = False
        self.number = None

    def get_key(self):
        return (self.x, self.y)
    
    def legal_neighbors(self, maze, traversed_path):
        neighbors = []
        if not self.walls['top'] and self.y > 0 and (self.x, self.y - 1) not in traversed_path :
            neighbors.append(maze.cells[(self.x, self.y - 1)])
        if not self.walls['right'] and self.x < maze.grid_size_x - 1 and (self.x + 1, self.y) not in traversed_path:
            neighbors.append(maze.cells[(self.x + 1, self.y)])
        if not self.walls['bottom'] and self.y < maze.grid_size_y - 1 and (self.x, self.y + 1) not in traversed_path:
            neighbors.append(maze.cells[(self.x, self.y + 1)])
        if not self.walls['left'] and self.x > 0 and (self.x - 1, self.y) not in traversed_path:
            neighbors.append(maze.cells[(self.x - 1, self.y)])
        return neighbors


class Maze:
    grid_size_x: int
    grid_size_y: int
    cells: dict[tuple[int, int], Cell]
    start_cell: Cell
    end_cell: Cell
    numbers: list[int]
    
    def __init__(self, grid_size_x=15, grid_size_y=12):
        self.set_grid_size(grid_size_x, grid_size_y)
        self.reset_cells()
        self.numbers = []
        
    def set_grid_size(self, x, y):
        self.grid_size_x = x
        self.grid_size_y = y
        
    def reset_cells(self):
        self.cells = {(x, y): Cell(x, y) for x in range(self.grid_size_x) for y in range(self.grid_size_y)}
        self.start_cell = None
        self.end_cell = None

    def set_start(self, x, y):
        if self.start_cell is not None:
            self.start_cell.is_start = False
        self.start_cell = self.cells[(x, y)]
        self.start_cell.is_start = True

    def set_end(self, x, y):
        if self.end_cell is not None:
            self.end_cell.is_end = False
        self.end_cell = self.cells[(x, y)]
        self.end_cell.is_end = True

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
                
            self.set_start(start_cell_x, start_cell_y)
            self.set_end(end_cell_x, end_cell_y)

            for cell in self.cells.values():
                if cell.number is not None:
                    self.numbers.append(cell.number)
            self.numbers.sort()
            
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

    def solve_dfs(self):
        solution = Solution()
        traversed_path: list[tuple[int,int]] = []
        last_seen_number = 0
        stack = [self.start_cell]
        # while we have cells to traverse
        while stack:
            current = stack.pop()
            # check if we are able to go to this cell
            if current in traversed_path or (current.number is not None and current.number != last_seen_number+1):
                continue
            # move to new cell
            traversed_path.append(current)
            last_seen_number = current.number if current.number is not None else last_seen_number
            # if we are at the end, we have the solution
            if current.is_end:
                solution.path = traversed_path
                return solution
            # check for legal neighbors
            legal_neighbors = current.legal_neighbors(self, traversed_path)
            # if there are legal neighbors, add them to the stack
            if legal_neighbors:
                for neighbor in legal_neighbors:
                    stack.append(neighbor)
            # if there aren't any legal neighbors, we need to correct the traversed path to match the last correct cell
            else:
                while traversed_path[-1] != stack[-1]:
                    removing_cell = traversed_path.pop()
                    if self.cells[removing_cell].number is not None:
                        last_seen_number = self.cells[removing_cell].number - 1
        return solution