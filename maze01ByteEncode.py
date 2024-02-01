'''
this maze is a 15x12 maze

maze is encoded as a byte array
each byte represents a cell in the maze

for the first four bits, 0b0000, the bits represent the walls
only internal walls will be represented, the outside walls will be assumed
    top:            0b1000
    right:          0b0100
    bottom:         0b0010
    left:           0b0001
    
the last four bits represent the number inside the cell. If it is 0, then the cell has no number
'''

def writeMazeToFile():
    row_ = [0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,
            0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,0b00000000,]
    
    mazeRows = []
    # row 1
    mazeRows.append([  0b00000000,0b00100000,0b00100000,0b00000000,0b00100000,0b00100000,0b01000000,
            0b00010000,0b00100000,0b00100000,0b01000000,0b00010000,0b00100000,0b00100000,0b00000000,])
    # row 2
    mazeRows.append([  0b01000000,0b10010000,0b11000000,0b01010000,0b10010000,0b11000000,0b01010000,
            0b01010000,0b10010000,0b11000000,0b01010000,0b01010000,0b10010000,0b11000000,0b00010000,])
    # row 3
    mazeRows.append([  0b01000000,0b01010000,0b01010000,0b01010000,0b01010000,0b01010000,0b01010000,
            0b01010000,0b01010000,0b00110000,0b00100000,0b00100000,0b01100000,0b01010000,0b00010000,])
    # # row 4
    mazeRows.append([  0b00000000,0b01100000,0b01010000,0b00110000,0b01100000,0b01010000,0b00110000,
            0b01100000,0b00110000,0b10000000,0b10100000,0b10100000,0b10100000,0b01000110,0b00010000,])
    with open('maze01', 'wb') as mazeFile:
        mazeFile.write(int(15).to_bytes(1, 'big'))
        mazeFile.write(int(12).to_bytes(1, 'big'))
        for row in mazeRows:
            mazeFile.write(bytearray(row))
    
    
def readCellsFromBytes():
    with open('maze01', 'rb') as maze_file:
        grid_size_x_byte = maze_file.read(1)
        grid_size_y_byte = maze_file.read(1)
        
        grid_size_x = int.from_bytes(grid_size_x_byte, "big")
        grid_size_y = int.from_bytes(grid_size_y_byte, "big")
        
        
        start_cell_x_byte = maze_file.read(1)
        start_cell_y_byte = maze_file.read(1)
        
        start_cell_x = int.from_bytes(start_cell_x_byte, "big")
        start_cell_y = int.from_bytes(start_cell_y_byte, "big")
        
        
        end_cell_x_byte = maze_file.read(1)
        end_cell_y_byte = maze_file.read(1)
        
        end_cell_x = int.from_bytes(end_cell_x_byte, "big")
        end_cell_y = int.from_bytes(end_cell_y_byte, "big")
        
        i = 0
        row_num = 1
        while (byte := maze_file.read(1)):
            if i == grid_size_x:
                i = 0
            if i == 0:
                print(f'Row {row_num}: ')
                row_num += 1
            byte_str = bin(int.from_bytes(byte, 'big'))[2:].rjust(8, '0')
            firstFour = byte_str[:4]
            lastFour = byte_str[4:]
            print(f'firstFour: {firstFour}, lastFour: {lastFour}')
            i += 1
        return grid_size_x, grid_size_y

def main():
    writeMazeToFile()
    xSize, ySize = readCellsFromBytes()
    print(f'xSize: {xSize}, ySize: {ySize}')

if __name__ == '__main__':
    main()