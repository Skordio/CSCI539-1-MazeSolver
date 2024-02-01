from enum import Enum
from typing import Literal

class Cell:
    isStart = False
    isEnd = False
    number = 0
    walls = {'top': False, 'right': False, 'bottom': False, 'left': False}
    
    def __init__(self, x, y, xSize, ySize):
        self.x = x
        self.y = y
        if x == 0:
            self.walls.left = True
        if x == xSize-1:
            self.walls.right = True
        if y == 0:
            self.walls.top = True
        if y == ySize-1:
            self.walls.bottom = True

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def setWall(self, wall:Literal['top', 'right', 'bottom', 'left'], value:bool):
        self.walls[wall] = value
        
    def setStart(self):
        self.isStart = True
        
    def setEnd(self):
        self.isEnd = True


class Maze:
    xSize = 0
    ySize = 0
    cells: list[list[Cell]] = []
    
    def __init__(self, xSize, ySize, startCell:tuple[int, int], endCell:tuple[int, int]):
        self.xSize = xSize
        self.ySize = ySize
        self.cells = [[Cell(x, y, xSize, ySize) for x in range(xSize)] for y in range(ySize)]
        self.getCell(startCell[0], startCell[1]).setStart()
        self.getCell(endCell[0], endCell[1]).setEnd()
    
        
    def getCell(self, x, y) -> Cell:
        return self.cells[y][x]