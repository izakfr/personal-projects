from __future__ import print_function
import numpy as np
import math as m

# 3x3 Grid of numbers, a sudoku board consists of 9 of these
class Nonet():
    def __init__(self):
        self.arr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# this function return true if there is no instance of this number in the row
# we do not check the nonet that the number is in
def checkRow(puzzle, x_nonet, y_nonet, row, num):
    for i in range(0, 3):
        for j in range(0, 3):
            if(i != y_nonet):
                if(int(puzzle[x_nonet][i].arr[row][j]) == num):
                    return 0
    return 1

# this function returns true if there is no instance of this number in the column
# we do not check the nonet that the number is in
def checkCol(puzzle, x_nonet, y_nonet, col, num):
    for i in range(0, 3):
        for j in range(0, 3):
            if(i != x_nonet):
                if(int(puzzle[i][y_nonet].arr[j][col]) == num):
                    return 0
    return 1

# Given and x and y nonet, check if the num is in its respective Nonet
def inNonet(puzzle, x_nonet, y_nonet, num):
    for i in range(0, 3):
        for j in range(0, 3):
            if(int(puzzle[x_nonet][y_nonet].arr[i][j]) == num):
                return 1
    return 0

# Run the crosshatching algo once
def crosshatching(puzzle):
    no_change = 1
    for i in range(0, 3):
        for j in range(0, 3):
            for x in range(0, 3):
                for y in range(0, 3):
                    if int(puzzle[i][j].arr[x][y]) == 0:
                        # we need to see if just one number can fit in here
                        test_num = 0
                        valid = 0
                        for num in range(1, 10):
                            if inNonet(puzzle, i, j, num) == 0:
                                if checkRow(puzzle, i, j, x, num) & checkCol(puzzle, i, j, y, num):
                                    if valid == 0:
                                        valid = 1
                                        test_num = num
                                    else:
                                        # there are two valid numbers, therefore
                                        # we must move on
                                        valid = 0
                                        break
                        if valid == 1:
                            # there is only one valid number so we set it to this
                            puzzle[i][j].arr[x][y] = test_num
                            no_change = 0
    return no_change

# this function prints the puzzle
def printPuzzle(puzzle, f):
    for x in range(0, 3):
        for y in range(0, 3):
            f.write("\n")
            for i in range(0, 3):
                for j in range(0, 3):
                    f.write(str(puzzle[x][i].arr[y][j]) + " ")

############################### Start the script below #########################

def solve():
    """Below we will solve the sudoku puzzle using crosshatching
        the basic method is to start with the 3x3 upper nonet and
        based on if there is one place each number could be by crossing
        each row or column it cannot be in, if there is only one space left
        then we place, if not move on"""
    puzzle = np.empty((3,3), dtype=object)

    for i in range(0, 3):
        for j in range(0,3):
            puzzle[i][j] = Nonet()

    data = open("puzzle.txt", "r")

    for x in range(0, 9):
        for y in range(0, 9):
            # read the number and put it into the array
            num = data.read(1)
            # the input needs to wind through the puzzle in the way it is set up
            # in objects
            puzzle[int(m.floor(x/3))][int(m.floor(y/3))].arr[(x%3)][(y%3)] = num
            num = data.read(1) # this reads the space to discard

    while(1):
        if(crosshatching(puzzle) == 1):
            break

    sol = open("puzzle_solution.txt", "w")
    printPuzzle(puzzle, sol)
    sol.close()
    data.close()

if __name__ == "__main__":
    solve()
