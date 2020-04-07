#  Created by Henry Rivera on 3/21/20.
#  File Name: A*_Search_Algorithm
#  Description: A* Search Algorithm Implementation to Solve 15 Puzzle Problem
#  Copyright © 2019 Henry Rivera. All rights reserved

import copy

class State(object):
    def __init__(self, puz, depth):
        self.puz = puz
        self.possiMove = []
        self.curreMoves = []
        self.depth = depth
        self.aStar = 0

    def __gt__(self, other):
        if self.aStar > other.aStar:
            return True
        else:
            return False

    def generatePossiMove(self): # modified
        posiMove = []
        if self.puz[0][0] != '0' and self.puz[1][0] != '0' \
                and self.puz[2][0] != '0' and self.puz[3][0] != '0':
            posiMove.append('L')
        if self.puz[0][2] != '0' and self.puz[1][2] != '0' \
                and self.puz[2][2] != '0' and self.puz[3][2] != '0':
            posiMove.append('R')
        if '0' not in self.puz[0]:
            posiMove.append('U')
        if '0' not in self.puz[3]:
            posiMove.append('D')
        self.possiMove = posiMove

    def function(self, goal_board):
        mah = 0
        for i in range(1, 16):
            sLoc = find(self.puz, str(i))
            gLoc = find(goal_board, str(i))
            mah = mah + abs(sLoc[0] - gLoc[0]) + abs(sLoc[1] - gLoc[1])
        print(mah)
        self.aStar = self.depth + mah


def find(puz, x):
    for i in range(4):
        for j in range(4):
            if puz[i][j] == x:
                return [i, j]


def moveZero(currBoard, move):
    zero = find(currBoard, '0')
    # print("Inside moveZero:", currBoard)
    newBoard = copy.deepcopy(currBoard)
    if move == 'U':
        newBoard[zero[0]][zero[1]] = newBoard[zero[0]-1][zero[1]]
        newBoard[zero[0]-1][zero[1]] = '0'
    elif move == 'D':
        newBoard[zero[0]][zero[1]] = newBoard[zero[0]+1][zero[1]]
        newBoard[zero[0]+1][zero[1]] = '0'
    elif move == 'L':
        newBoard[zero[0]][zero[1]] = newBoard[zero[0]][zero[1]-1]
        newBoard[zero[0]][zero[1]-1] = '0'
    elif move == 'R':
        newBoard[zero[0]][zero[1]] = newBoard[zero[0]][zero[1]+1]
        newBoard[zero[0]][zero[1]+1] = '0'
    return newBoard


def generateNewState(currState, move, goal_board):
    print("currState.aStar: ", currState.aStar)
    newBoard = moveZero(currState.puz, move)
    newState = State(newBoard, currState.depth+1)
    # print("Inside generateNewState:", currState.curreMoves)
    currMoves = copy.deepcopy(currState.curreMoves)
    currMoves.append(move)
    newState.curreMoves = currMoves
    newState.function(goal_board)
    newState.generatePossiMove()
    return newState


def main(filename):
    f = open(filename, "r")
    content = f.read().splitlines()
    states = []
    for line in content:
        states.append(line.split())
    initial = states[0:4]
    goal = states[5:9]
    start = State(initial, 0)
    start.generatePossiMove()
    start.function(goal)
    opened = [start]
    closed = [initial]
    nodeCnt = 1
    arr = []
    while opened:
        opened.sort(reverse=True)
        current_state = opened.pop()
        arr.append(current_state.aStar)
        if current_state.puz == goal:
            outputFilename = "Output" + filename[5] + ".txt"
            output = open(outputFilename, "w+")
            for r in initial:
                output.write(' '.join(r) + "\r\n")
            output.write("\r\n")
            for row in goal:
                output.write(' '.join(row) + "\r\n")
            output.write("\r\n")
            output.write("Correct Moves: " + ', '.join(current_state.curreMoves) + "\r\n")
            output.write("Depth: " + str(current_state.depth) + "\r\n")
            output.write("Nodes created: " + str(nodeCnt) + "\r\n")
            print(arr)
            output.close()
            return
        for move in current_state.possiMove:
            newState = generateNewState(current_state, move, goal)
            if newState.puz not in closed:
                nodeCnt += 1
                closed.append(newState.puz)
                opened.append(newState)


main("Input2.txt")
