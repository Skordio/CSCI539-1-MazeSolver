from enum import Enum
import time
from typing import Literal, List, Dict, Tuple
from collections import deque

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': False, 'right': False, 'bottom': False, 'left': False}        
        self.is_start = False
        self.is_end = False
        self.number = None

    def __str__(self):
        return str(self.coords())
    
    def __repr__(self):
        return self.__str__()

    def get_key(self):
        return (self.x, self.y)
    
    def distance_to_cell(self, cell):
        return ((self.x - cell.x)**2 + (self.y - cell.y)**2)**0.5
    
    def legal_neighbors(self, maze, traversed_path=[], last_seen_number=None):
        neighbors = []
        if not self.walls['top'] and self.y > 0:
            neighbors.append(maze.cells[(self.x, self.y - 1)])
        if not self.walls['right'] and self.x < maze.grid_size_x - 1:
            neighbors.append(maze.cells[(self.x + 1, self.y)])
        if not self.walls['bottom'] and self.y < maze.grid_size_y - 1:
            neighbors.append(maze.cells[(self.x, self.y + 1)])
        if not self.walls['left'] and self.x > 0:
            neighbors.append(maze.cells[(self.x - 1, self.y)])

        i = len(neighbors) - 1
        while i >= 0:
            remove = False
            if neighbors[i] in traversed_path:
                remove = True

            if last_seen_number is not None and maze.numbers:
                if neighbors[i].number is not None and neighbors[i].number != last_seen_number+1:
                    remove = True
                if neighbors[i].is_end and last_seen_number != maze.numbers[-1]:
                    remove = True
            
            if remove:
                neighbors.pop(i)

            i -= 1

        return neighbors
    
    def coords(self):
        return (self.x, self.y)

class Path:
    path: list[Cell]
    last_seen_number: int

    def __init__(self, path=[], last_seen_number=0):
        self.path = path
        self.last_seen_number = last_seen_number

    def __str__(self):
        return str(self.path_coords())
    
    def __repr__(self):
        return self.__str__()

    def path_coords(self):
        return [cell.coords() for cell in self.path]


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
        
    def add_number(self, number):
        print(f'before: {self.numbers}')
        self.numbers.append(number)
        self.numbers.sort()
        print(f'after: {self.numbers}')
        
    def remove_number(self, number):
        print(f'before: {self.numbers}')
        self.numbers.remove(number)
        self.numbers.sort()
        print(f'after: {self.numbers}')
        
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
        with open(f'mazes\{filename}', 'rb') as maze_file:
            grid_size_x_byte = maze_file.read(1)
            grid_size_y_byte = maze_file.read(1)
            
            grid_size_x = int.from_bytes(grid_size_x_byte, "big")
            grid_size_y = int.from_bytes(grid_size_y_byte, "big")
            
            self.__init__(grid_size_x, grid_size_y)
            
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
        with open(f'mazes\{filename}', 'wb') as maze_file:
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
        with open('solver_output_dfs.txt', 'w') as f:
            traversed = Path(path=[], last_seen_number=0)
            last_seen_number = 0
            stack = [(None, self.start_cell)]
            iterations = 0
            while stack:
                iterations += 1
                current_cell = stack.pop()[1]
                traversed.path.append(current_cell)
                last_seen_number = current_cell.number if current_cell.number is not None else last_seen_number
                # if we are at the end, we have the solution
                if current_cell.is_end:
                    break
                # check for legal neighbors
                legal_neighbors = current_cell.legal_neighbors(self, traversed.path, last_seen_number)
                # if there are legal neighbors, add them to the stack
                if legal_neighbors:
                    for neighbor in legal_neighbors:
                        stack.append((current_cell, neighbor))
                # if there aren't any legal neighbors, we need to correct the traversed path to match the next cell on the stack
                elif stack:
                    while traversed.path and stack[-1][0] != traversed.path[-1]:
                        removing_cell = traversed.path.pop()
                        if removing_cell.number is not None:
                            last_seen_number = removing_cell.number - 1
                
            f.write(f'iterations: {iterations}\n')
            return traversed
    
    def solve_bfs(self):
        with open('solver_output_bfs.txt', 'w') as f:
            possible_solutions = [Path([self.start_cell])]
            new_solutions = []
            iterations = 0

            while possible_solutions:
                # for each path in the list
                for solution in possible_solutions:
                    iterations += 1
                    # get the last cell in the path
                    current = solution.path[-1]
                    # if the last cell is the end, we have the solution
                    if current.is_end:
                        f.write(f'iterations: {iterations}\n')
                        return solution
                    # for each legal neighbor of the last cell, create a new path and create a new list of possible solutions for the next iteration
                    for neighbor in current.legal_neighbors(self, solution.path, solution.last_seen_number):
                        new_path = Path(solution.path + [neighbor], neighbor.number if neighbor.number is not None else solution.last_seen_number)
                        new_solutions.append(new_path)
                # set the list of possible solutions to the list of new solutions
                possible_solutions = new_solutions
                new_solutions = []
                # repeat until we find the solution

            f.write(f'iterations: {iterations}\n')
            return Path()
    
    def rate_legal_neighbors(self, legal_neighbors, last_seen_number):
        rated_neighbors = []
        next_cell = None
        if self.numbers and last_seen_number < self.numbers[-1]:
            next_cell_num = last_seen_number + 1
            for cell in self.cells.values():
                if cell.number == next_cell_num:
                    next_cell = cell
                    break
        elif (self.numbers and last_seen_number == self.numbers[-1]) or not self.numbers:
            next_cell = self.end_cell

        if next_cell is not None:
            for neighbor in legal_neighbors:
                rated_neighbors.append((neighbor, neighbor.distance_to_cell(next_cell)))
            rated_neighbors.sort(key=lambda x: x[1], reverse=True)
            return [x[0] for x in rated_neighbors]
        else:
            rated_neighbors = legal_neighbors
            
    
    def solve_human_search(self):
        with open('solver_output_human.txt', 'w') as f:
            traversed = Path(path=[], last_seen_number=0)
            last_seen_number = 0
            stack = [(None, self.start_cell)]
            iterations = 0
            while stack:
                iterations += 1
                current_cell = stack.pop()[1]
                traversed.path.append(current_cell)
                last_seen_number = current_cell.number if current_cell.number is not None else last_seen_number
                # if we are at the end, we have the solution
                if current_cell.is_end:
                    break
                # check for legal neighbors
                legal_neighbors = current_cell.legal_neighbors(self, traversed.path, last_seen_number)
                legal_neighbors = self.rate_legal_neighbors(legal_neighbors, last_seen_number)
                # if there are legal neighbors, add them to the stack
                if legal_neighbors:
                    for neighbor in legal_neighbors:
                        stack.append((current_cell, neighbor))
                # if there aren't any legal neighbors, we need to correct the traversed path to match the next cell on the stack
                elif stack:
                    while traversed.path and stack[-1][0] != traversed.path[-1]:
                        removing_cell = traversed.path.pop()
                        if removing_cell.number is not None:
                            last_seen_number = removing_cell.number - 1
                
            
            f.write(f'iterations: {iterations}\n')
            return traversed