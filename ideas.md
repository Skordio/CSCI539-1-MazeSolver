# Brainstorm area

this is where I will brainstorm ideas for Maze Solver and Maze Creator

## Encoding ideas

to encode the maze, we could use a file consisting just of a series of bytes, where each byte represented one square of the maze. The order of the bytes would just go from the first one in the first row, then the next one in that row, until reaching the end of the row and then the next byte would be the first cell in the next row. The first four bits would indicate which sides of the cell have walls, and the next four bits could indicate if that cell had a numerical value in it.

The maze constructor can just take that file. In the maze definition file, we could have the first byte represent the width of a row in the maze. We don't need the height, because we use the width and just read from the maze definition file, jumping down a row whenever we reach the length of a row.

## Making solving better

Problem: in this type of maze, you can wall yourself off so there is no way to solve it really easily. This will be a problem for dfs but not for bfs I think

Possible solution: record turns before getting to the next number where all possible turns weren't explored. If we fuck up and it is impossible after getting to the current number, go back to the most recent turn before the number that wasn't explored and continue from there, exploring the next turn that wasn't taken

## Measuring Unexpected Things

One idea for measuring "unexpected things" would have to be measuring how close the path comes to the end square before it is the end. So like if you have a path where halfway through it passes by the end before returning to finally end, that would be unexpected.