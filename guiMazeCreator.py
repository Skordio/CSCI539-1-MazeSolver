import tkinter as tk
from tkinter import simpledialog

class Cell:
    def __init__(self):
        # Each key represents a wall; True means the wall exists
        self.walls = {'top': False, 'right': False, 'bottom': False, 'left': False}        
        self.is_start = False
        self.is_end = False
        self.number = None
        self.highlight_id = None  # Track the highlight rectangle ID

class MazeEditor:
    def __init__(self, master):
        self.master = master
        self.highlighted_cell = None  # Track the highlighted cell
        self.grid_size_x = 15  # Default grid size
        self.grid_size_y = 12  # Default grid size
        self.cell_size = 40  # Visual size of cells in pixels
        self.cells = {}  # Stores Cell objects
        self.create_widgets()
        self.reset_grid()  # This method now initializes cells and draws the grid

    def create_widgets(self):
        # Create a frame as a container for the canvas
        self.frame = tk.Frame(self.master, bd=0, highlightbackground="black", highlightthickness=1)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=5, ipady=0)

        # Create the canvas within the frame
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True,)
        
        # self.canvas = tk.Canvas(self.master, width=400, height=400)
        # self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.reset_button = tk.Button(self.master, text="Reset Grid", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT)

        self.size_button = tk.Button(self.master, text="Set Grid Size", command=self.prompt_grid_size)
        self.size_button.pack(side=tk.RIGHT)
        
        self.start_button = tk.Button(self.master, text="Set Start", command=self.set_start_cell)
        self.start_button.pack(side=tk.LEFT)

        self.end_button = tk.Button(self.master, text="Set End", command=self.set_end_cell)
        self.end_button.pack(side=tk.LEFT)

        self.number_button = tk.Button(self.master, text="Place Number", command=self.place_number)
        self.number_button.pack(side=tk.LEFT)
        
        self.canvas.bind("<Button-3>", self.toggle_highlight)  # Right-click to highlight a cell

    def reset_grid(self):
        self.cells = {(x, y): Cell() for x in range(self.grid_size_x) for y in range(self.grid_size_y)}
        self.canvas.delete("all")
        self.draw_grid()  # Moved the draw_grid call here

    def prompt_grid_size(self):
        sizeX = simpledialog.askinteger("Input", "Enter grid size x:", parent=self.master, minvalue=5, maxvalue=20)
        sizeY = simpledialog.askinteger("Input", "Enter grid size y:", parent=self.master, minvalue=5, maxvalue=20)
        if sizeX and sizeY:
            self.set_grid_size(sizeX, sizeY)

    def set_grid_size(self, sizeX, sizeY):
        self.grid_size_x = int(sizeX)
        self.grid_size_y = int(sizeY)
        canvas_width = self.cell_size * self.grid_size_x
        canvas_height = self.cell_size * self.grid_size_y
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.master.geometry(f"{canvas_width+40}x{canvas_height+70}")  # Adjust window size, +50 for buttons
        self.reset_grid()

    def draw_grid(self):
        for i in range(self.grid_size_x):
            for j in range(self.grid_size_y):
                x1, y1 = i * self.cell_size, j * self.cell_size
                self.draw_cell(i, j, x1, y1)
                cell = self.cells[(i, j)]
                if cell.highlight_id:
                    # Redraw the highlight rectangle to ensure it's on top
                    self.canvas.tag_raise(cell.highlight_id)

    def draw_cell(self, i, j, x1, y1):
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        cell_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="light grey", tags=("cell", f"{i},{j}"))
        self.cells[(i, j)].id = cell_id
        cell = self.cells[(i, j)]
        if cell.is_start:
            self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text="S", fill="green", tags=(f"{cell.id}-start"))
        elif cell.is_end:
            self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text="E", fill="red", tags=(f"{cell.id}-end"))
        elif cell.number is not None:
            self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text=str(cell.number), tags=(f"{cell.id}-number"))
        self.update_cell_walls(i, j)

    def update_cell_walls(self, i, j):
        cell = self.cells[(i, j)]
        x1, y1 = i * self.cell_size, j * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size

        # Removing previous walls
        self.canvas.delete(f"wall-{i},{j}-top")
        self.canvas.delete(f"wall-{i},{j}-right")
        self.canvas.delete(f"wall-{i},{j}-bottom")
        self.canvas.delete(f"wall-{i},{j}-left")

        # Drawing walls based on the cell's wall properties
        if cell.walls['top']:
            self.canvas.create_line(x1, y1, x2, y1, fill="black", tags=(f"wall-{i},{j}-top"))
        if cell.walls['right']:
            self.canvas.create_line(x2, y1, x2, y2, fill="black", tags=(f"wall-{i},{j}-right"))
        if cell.walls['bottom']:
            self.canvas.create_line(x1, y2, x2, y2, fill="black", tags=(f"wall-{i},{j}-bottom"))
        if cell.walls['left']:
            self.canvas.create_line(x1, y1, x1, y2, fill="black", tags=(f"wall-{i},{j}-left"))

        self.canvas.bind("<Button-1>", self.toggle_wall)

    def toggle_wall(self, event):
        # Find the cell that was clicked
        
        i, j = (event.x // self.cell_size, event.y // self.cell_size)
        cell = self.cells[(i, j)]

        alsoUpdate = {'i':i, 'j':j}

        # Determine which wall to toggle based on the click position within the cell
        x, y = event.x % self.cell_size, event.y % self.cell_size
        if x < self.cell_size / 4 and i > 0:
            cell.walls['left'] = not cell.walls['left']
            if i > 0:
                otherCell = self.cells[(i-1, j)]
                otherCell.walls['right'] = not otherCell.walls['right']
                alsoUpdate['i'] = i-1
        elif x > 3 * self.cell_size / 4 and i < self.grid_size_x - 1:
            cell.walls['right'] = not cell.walls['right']
            if i < self.grid_size_x - 1:
                otherCell = self.cells[(i+1, j)]
                otherCell.walls['left'] = not otherCell.walls['left']
                alsoUpdate['i'] = i+1
        elif y < self.cell_size / 4 and j > 0:
            cell.walls['top'] = not cell.walls['top']
            if j > 0:
                otherCell = self.cells[(i, j-1)]
                otherCell.walls['bottom'] = not otherCell.walls['bottom']
                alsoUpdate['j'] = j-1
        elif y > 3 * self.cell_size / 4 and j < self.grid_size_y - 1:
            cell.walls['bottom'] = not cell.walls['bottom']
            if j < self.grid_size_y - 1:
                otherCell = self.cells[(i, j+1)]
                otherCell.walls['top'] = not otherCell.walls['top']
                alsoUpdate['j'] = j+1

        self.update_cell_walls(i, j)
        if alsoUpdate['i'] != i or alsoUpdate['j'] != j:
            self.update_cell_walls(alsoUpdate['i'], alsoUpdate['j'])
            
    def toggle_highlight(self, event):
        i, j = (event.x // self.cell_size, event.y // self.cell_size)
        
        if self.highlighted_cell and self.highlighted_cell == self.cells[(i, j)]:
            # De-highlight the currently highlighted cell
            self.canvas.delete(self.highlighted_cell.highlight_id)
            self.highlighted_cell.highlight_id = None
            self.highlighted_cell = None
        else:
            # Highlight a new cell
            if self.highlighted_cell:
                # Remove existing highlight
                self.canvas.delete(self.highlighted_cell.highlight_id)
                self.highlighted_cell.highlight_id = None

            self.highlighted_cell = self.cells[(i, j)]

            # Add new highlight
            x1, y1 = i * self.cell_size, j * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.highlighted_cell.highlight_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)

    def set_start_cell(self):
        if self.highlighted_cell:
            self.canvas.delete(f"{self.highlighted_cell.id}-start")
            if self.highlighted_cell.is_start:
                # Remove start marker if it's already set
                self.highlighted_cell.is_start = False
            else:
                # Set start marker
                self.reset_start_end_flags()
                self.highlighted_cell.is_start = True
            self.draw_grid()

    def set_end_cell(self):
        if self.highlighted_cell:
            self.canvas.delete(f"{self.highlighted_cell.id}-end")
            if self.highlighted_cell.is_end:
                # Remove end marker if it's already set
                self.highlighted_cell.is_end = False
            else:
                # Set end marker
                self.reset_start_end_flags()
                self.highlighted_cell.is_end = True
            self.draw_grid()

    def place_number(self):
        if self.highlighted_cell:
            self.canvas.delete(f"{self.highlighted_cell.id}-number")
            if self.highlighted_cell.number is not None:
                # Remove the number if it's already placed
                self.highlighted_cell.number = None
            else:
                # Place a new number
                number = simpledialog.askinteger("Input", "Enter cell number:", parent=self.master, minvalue=1, maxvalue=100)
                if number is not None:
                    self.highlighted_cell.number = number

        # Update the grid with changes
        i, j = self.find_cell_coordinates(self.highlighted_cell)
        self.update_cell_number(self.highlighted_cell, i, j)
        self.draw_grid()

    def update_cell_number(self, cell, i, j):
        # Calculate the center coordinates of the cell
        x_center = i * self.cell_size + self.cell_size // 2
        y_center = j * self.cell_size + self.cell_size // 2

        # Delete any existing number text
        if hasattr(cell, 'number_id') and cell.number_id:
            self.canvas.delete(cell.number_id)

        # Create new text in the cell
        cell.number_id = self.canvas.create_text(x_center, y_center, text=str(cell.number))

    def reset_start_end_flags(self):
        for cell in self.cells.values():
            cell.is_start = False
            cell.is_end = False
        
    def find_cell_coordinates(self, cell):
        for i in range(self.grid_size_x):
            for j in range(self.grid_size_y):
                if self.cells[(i, j)] == cell:
                    return i, j
        return None, None  # Just in case the cell is not found



def main():
    root = tk.Tk()
    root.title("Maze Editor")
    app = MazeEditor(root)
    app.set_grid_size(15, 12)  # Default grid size
    root.mainloop()

if __name__ == "__main__":
    main()
