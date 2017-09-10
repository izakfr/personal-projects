import numpy as np

#define the puzzle array so that we can index it
puzzle = np.empty((9, 9), dtype=int)

#Open the TXT file and grab the puzzle data
data = open("puzzle.txt", "r")

#take the data and put it into the array so far
#we want to read a total of 81 numbers in
for x in range(0, 9):
    for y in range(0, 9):
        #read the number and put it into the array
        num = data.read(1)
        puzzle[x][y] = num
        num = data.read(1) #this reads the space to discard

print(puzzle)
data.close()
