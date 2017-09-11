import numpy as np
import math as m

class Nonet():
    def __init__(self):
        self.arr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

#define the puzzle as a 3x3 array
puzzle = np.empty((3,3), dtype=object)

#fill the puzzle with Nonets
for i in range(0, 3):
    for j in range(0,3):
        puzzle[i][j] = Nonet()


#Open the TXT file and grab the puzzle data
data = open("puzzle.txt", "r")

#take the data and put it into the array so far
#we want to read a total of 81 numbers in
for x in range(0, 9):
    for y in range(0, 9):
        #read the number and put it into the array
        num = data.read(1)
        #the input needs to wind through the puzzle in the way it is set up
        #in objects
        puzzle[int(m.floor(x/3))][int(m.floor(y/3))].arr[(x%3)][(y%3)] = num
        num = data.read(1) #this reads the space to discard

#Below we will solve the sudoku puzzle using crosshatching
#The basic method is to start with the 3x3 upper nonet and
#based on if there is one place each number could be by crossing
#each row or column it cannot be in, if there is only one space left
#then we place, if not move on

#this function return true if the given number can be placed in the given spot
# def canPlace(x, y, num):
#     "Return if coord x, y is a valid spot for num"
#     for i in range
#     return false

#returns the nonet letter that the num is in
# def returnNonet(x, y, num):
#     "Return true if val is in nonet that coresponds to a x, y coord"
#     if(x < 3):
#         if(y < 3):
#             return "A"
#         elif(y < 6):
#             return "B"
#         else:
#             return "C"
#     elif(x < 6):
#         if(y < 3):
#             return "D"
#         elif(y < 6):
#             return "E"
#         else:
#             return "F"
#     else:
#         if(y < 3):
#             return "G"
#         elif(y < 6):
#             return "H"
#         else:
#             return "I"
#
data.close()
