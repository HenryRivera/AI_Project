#  Created by Henry Rivera on 3/21/20.
#  File Name: A*_Search_Algorithm
#  Description: A* Search Algorithm Implementation to Solve 15 Puzzle Problem
#  Copyright © 2019 Henry Rivera. All rights reserved


class A_Search:
    def __init__(self, data, depth, fval):
        """ Initialize the node with the data, depth of the node and the calculated fvalue """
        self.data = data
        self.depth = depth
        self.fval = fval

    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x, y = self.find(self.data, '0')
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        '''         Down        Up          Left        Up'''
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.moveZero(self.data, x, y, i[0], i[1])
            if child:
                child_node = A_Search(child, self.depth + 1, 0)
                children.append(child_node)
        # print("depth:", self.depth)
        # print("f(n):", self.fval)
        return children

    def moveZero(self, puz, x1, y1, x2, y2):
        """ Move the 0 in the given direction and if the position value are out
            of limits the return None """
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = []
            temp_puz = self.duplicate(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def duplicate(self, root):
        """ Creates duplicate of given node"""
        tmp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            tmp.append(t)
        return tmp

    def find(self, puz, x):
        """ Specifically used to find the position of the blank space """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, filename):
        """ Initialize the puzzle size by the specified size, unchecked and checked lists to empty """
        self.n = 4
        self.filename = filename
        self.unchecked = []
        self.checked = []

    def f(self, initial, goal):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return self.h(initial.data, goal) + initial.depth

    def h(self, initial, goal):
        """ Calculates the different between the given puzzles """
        tmp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if initial[i][j] != goal[i][j] and initial[i][j] != '0':
                    tmp += 1
        return tmp

    def generate_solution(self):
        """ Accept initial and Goal Puzzle state"""
        f = open(self.filename, "r")
        content = f.read().splitlines()
        states = []
        for line in content:
            states.append(line.split())
        initial = states[0:4]
        goal = states[5:9]

        initial = A_Search(initial, 0, 0)
        initial.fval = self.f(initial, goal)
        print("Initial:", initial.fval)
        print("Depth:", initial.depth)
        """ Put the initial node in the unchecked list"""
        self.unchecked.append(initial)
        while True:
            curr = self.unchecked[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in curr.data:
                for j in i:
                    print(j, end=" ")
                print("")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if self.h(curr.data, goal) == 0:
                break
            for i in curr.generate_child():
                i.fval = self.f(i, goal)
                self.unchecked.append(i)
            self.checked.append(curr)
            del self.unchecked[0]
        """ sort the unchecked list based on f value """
        self.unchecked.sort(key=lambda x: x.fval, reverse=False)


def main():
    puz = Puzzle("Input1.txt")
    puz.generate_solution()


main()
