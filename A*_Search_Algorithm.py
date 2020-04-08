#  Created by Henry Rivera on 3/21/20.
#  File Name: A*_Search_Algorithm
#  Description: A* Search Algorithm Implementation to Solve 15 Puzzle Problem
#  Copyright © 2019 Henry Rivera. All rights reserved

import copy


class GameBoard(object):
    """ I refer to the current state of the game board as node. Apologies for any inconvenience"""
    def __init__(self, board, depth):
        self.board = board  # state of board
        self.potential = []  # stores potential moves
        self.current = []  # current moves made
        self.depth = depth  # depth of shallowest nodes (puzzle)
        self.fVal = 0  # fVal of current node (puzzle)

    """ Allows us to compare nodes based on fVal to choose which to expand"""
    def __gt__(self, other):
        if self.fVal > other.fVal:
            return True
        else:
            return False

    """ Generates fVal of node passed in"""
    def genfVal(self, goalNode):
        manhattan = 0
        for i in range(1, 16):
            ''' finds current position of i'''
            currPos = find(self.board, str(i))
            ''' finds goals position of i'''
            goalPos = find(goalNode, str(i))
            manhattan = abs(currPos[0] - goalPos[0]) + abs(currPos[1] - goalPos[1]) + manhattan
        self.fVal = self.depth + manhattan

    """ Creates a list of potential directions we can move the 0 in"""
    def findPotential(self):
        moves = []
        if '0' not in self.board[0]:
            moves.append('U')
        if '0' not in self.board[3]:
            moves.append('D')
        if self.board[0][0] != '0' and self.board[1][0] != '0' \
                and self.board[2][0] != '0' and self.board[3][0] != '0':
            moves.append('L')
        if self.board[0][3] != '0' and self.board[1][3] != '0' \
                and self.board[2][3] != '0' and self.board[3][3] != '0':
            moves.append('R')
        self.potential = moves


""" Looks for the first occurrence of x"""
def find(node, x):
    for i in range(4):
        for j in range(4):
            if node[i][j] == x:
                return [i, j]


""" Having chosen to expand a node with the lowest fVal, we then move the 0"""
def moveZero(currNode, move):
    zero = find(currNode, '0')
    newNode = copy.deepcopy(currNode)
    if move == 'U':
        newNode[zero[0]][zero[1]] = newNode[zero[0]-1][zero[1]]
        newNode[zero[0]-1][zero[1]] = '0'
    elif move == 'D':
        newNode[zero[0]][zero[1]] = newNode[zero[0]+1][zero[1]]
        newNode[zero[0]+1][zero[1]] = '0'
    elif move == 'L':
        newNode[zero[0]][zero[1]] = newNode[zero[0]][zero[1]-1]
        newNode[zero[0]][zero[1]-1] = '0'
    else:  # Has to be right
        newNode[zero[0]][zero[1]] = newNode[zero[0]][zero[1]+1]
        newNode[zero[0]][zero[1]+1] = '0'
    return newNode


""" Having chosen to expand a node with the lowest fVal, we then create the new board"""
def expandNode(currNode, direction, goalNode):
    move = moveZero(currNode.board, direction)
    newNode = GameBoard(move, currNode.depth+1)
    currMoves = copy.deepcopy(currNode.current)
    currMoves.append(direction)
    newNode.current = currMoves
    newNode.genfVal(goalNode)
    newNode.findPotential()
    return newNode


def main(filename):
    f = open(filename, "r")
    content = f.read().splitlines()
    states = []
    for line in content:
        states.append(line.split())
    """ Reading initial and goal states from file"""
    initial = states[0:4]
    goal = states[5:9]
    """ Creating root node"""
    start = GameBoard(initial, 0)
    """ Looking for potential moves"""
    start.findPotential()
    """ And their fVals"""
    start.genfVal(goal)
    """ A* search algorithm uses opened and closed lists"""
    opened = [start]
    closed = [initial]
    nodeCnt = 1
    fVals = []
    while opened:
        opened.sort(reverse=True)
        currNode = opened.pop()
        fVals.append(str(currNode.fVal))
        """ Found our goal node"""
        if currNode.board == goal:
            outputFilename = "Output" + filename[5] + ".txt"
            output = open(outputFilename, "w+")
            for r in initial:
                output.write(' '.join(r) + "\r\n")
            output.write("\r\n")
            for row in goal:
                output.write(' '.join(row) + "\r\n")
            output.write("\r\n")
            output.write("Depth: " + str(currNode.depth) + "\r\n")
            output.write("Nodes created: " + str(nodeCnt) + "\r\n")
            output.write("Solution Path: " + ', '.join(currNode.current) + "\r\n")
            output.write("f(n) vals of solution path: " + ', '.join(fVals) + "\r\n")
            output.close()
            break
        for move in currNode.potential:
            newNode = expandNode(currNode, move, goal)
            if newNode.board not in closed:
                nodeCnt += 1
                closed.append(newNode.board)
                opened.append(newNode)


main("Input1.txt")
