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


def main():
    with open('maze01', 'wb') as mazeFile:
        row1 = [0b00000000,0b00100000,0b00100000,0b00000000,0b00100000,0b00100000,0b01000000,
                0b00010000,0b00100000,0b00100000,0b01000000,0b00010000,0b00100000,0b00100000,0b00000000,]
        row2 = [0b01000000,0b10010000,0b11000000,0b01010000,0b10010000,0b11000000,0b01010000,
                0b01010000,0b10010000,0b11000000,0b01010000,0b01010000,0b10010000,0b11000000,0b00010000,]


if __name__ == '__main__':
    main()