import sys
from random import *

def disp_game(board,n, start, target):
    'display board of size nxn with start and target'
    
    print('+'+(2*n-1)*'-'+'+')
    for y in range(n):
        print('|',end = '')
        for x in range(n):
            if board[(x,y)] == 'N':
                arrow = '\u2191'
            elif board[(x,y)] == 'S':
                arrow = '\u2193'
            elif board[(x,y)] == 'W':
                arrow = '\u2190'
            elif board[(x,y)] == 'E':
                arrow = '\u2192'
            if (x,y) == target:
                sys.stdout.shell.write('X', 'COMMENT')
                print('|', end = '')
            elif (x,y) == start:
                sys.stdout.shell.write(arrow, 'COMMENT')
                print('|', end = '')                
            else:
                print(arrow, end = '|')
        print()
        if y < n-1:
            print('|'+(2*n-1)*'-'+'|')
    print('+'+(2*n-1)*'-'+'+')
    
def create_game(n,k):
    'create random nxn board game which can be solved in at most k steps'
    
    sol = [(0,0)] # list of moves from (0,0) to target
    board  = {} # dictionary with keys (x,y) and values 'N','S','W','E'
    flip = (random() < 0.5)
    for _ in range(k):
        (x,y) = sol[-1]
        xnew,ynew = x,y
        while (xnew,ynew) == (x,y) or (xnew,ynew) in board:
            if flip:
                xnew = randrange(n)
                board[(x,y)] = 'W' if xnew < x else 'E'
            else:
                ynew = randrange(n)
                board[(x,y)] = 'N' if ynew < y else 'S'
        flip = not flip
        sol.append((xnew,ynew))
    target = (xnew,ynew)
    for x in range(n):
        for y in range(n):
            if (x,y) not in board:
                board[(x,y)] = choice('NSWE')
    print('Move from (0,0) to {}'.format(target))
    disp_game(board,n,(0,0),target)
    print('There is a solution in {} steps'.format(k))
    
    return board, sol

# importing double ended queue
from collections import deque

# function to find the path on the board from start to target
# takes in the board (dict of tuples) i.e. key = (x, y) and value = move direction N,S,E,W 
# and the target position (tuple)
def find_path(board, target):
    # start position is always (0, 0)
    start = (0, 0)
    # if start is the target, search is complete and we return start i.e. [(0, 0)]
    if start == target:
        return [start]
    
    # get the max size of the board using python list comprehension
    # takes the max of x and y from the keys of the board dict and adds 1
    # since we start counting from 0 and assigns the value to n so that we don't go off the board
    n = max(max(x for x, y in board.keys()), max(y for x, y in board.keys())) + 1
    
    # set to keep track of visited cells to avoid repetition
    visited = set()
    # double ended queue to keep track of cells to visit next
    queue = deque()
    # add the start cell to the queue with the path as a list containing the start cell i.e. initially [(0, 0)]
    queue.append((start, [start]))
    # adding the start cell to the visited set initially so that we don't visit it again
    # i.e. we don't add the start cell to the queue again 
    visited.add(start)
    
    # loops until the queue is empty
    while queue:
        # pop the leftmost cell from the queue which is also the current cell i.e. cur_cell 
        # along with the path taken to reach it i.e. path
        cur_cell, path = queue.popleft()
        # unpacking the x and y coordinates of the current cell i.e. cur_cell
        x, y = cur_cell
        
        # get the arrow direction of the current cell i.e. cur_cell, from the board dict and assign it to dir_arr
        dir_arr = board.get(cur_cell)
        
        # based on the direction of the arrow i.e dir_arr of the current cell i.e. cur_cell,
        # we get the all the possible next cells we can visit based on the direction of the current cell
        next_cells = []
        # for example: if the dir_arr is 'N' i.e. North, we list all the cells directly above the current cell
        # i.e. same x but y decreases (y-1, y-2, y-3, ... till 0)
        if dir_arr == 'N':
            next_cells = [(x, new_y) for new_y in range(y-1, -1, -1)]
        # for example: if the dir_arr is 'S' i.e. South, we list all the cells directly below the current cell
        # i.e. same x but y increases (y+1, y+2, y+3, ... till n)
        elif dir_arr == 'S':
            next_cells = [(x, new_y) for new_y in range(y+1, n)]
        # for example: if the dir_arr is 'W' i.e. West, we list all the cells left to the current cell
        # i.e. same y but x decreases (x-1, x-2, x-3, ... till 0)
        elif dir_arr == 'W':
            next_cells = [(new_x, y) for new_x in range(x-1, -1, -1)]
        # for example: if the dir_arr is 'E' i.e. East, we list all the cells right to the current cell
        # i.e. same y but x increases (x+1, x+2, x+3, ... till n)
        elif dir_arr == 'E':
            next_cells = [(new_x, y) for new_x in range(x+1, n)]
        
        # for each possible next cell in the next_cells list 
        for next_cell in next_cells:
            # check if the next cell is the target cell, if it is the target cell, 
            # we return the current path + target cell i.e. path + [next_cell] 
            if next_cell == target:
                return path + [next_cell]
            # if the next cell is not the target cell, we check if the next cell has not been visited i.e. not in visited set
            # if it has not been visited, we add it to the visited set and append it to the queue 
            # along with the new path (current path + next cell) i.e. path + [next_cell]
            if next_cell not in visited:
                visited.add(next_cell)
                queue.append((next_cell, path + [next_cell]))
    # exit if the queue is empty and the target cell is not found
    return None

# Successful Test Case 1: Generate 8x8 board with 4 legal steps solution
board1, sol1 = create_game(8, 4)
# since the sol1 returns a list of (x,y) from start position (0,0) to the target cell
# we get the target cell using sol1[-1]
target1 = sol1[-1]
path1 = find_path(board1, target1)
print('Legal Path:', path1)

# Successful Test Case 2: Generate 8x8 board with 5 legal steps solution
board2, sol2 = create_game(8, 5)
# since the sol2 returns a list of (x,y) from start position (0,0) to the target cell
# we get the target cell using sol2[-1]
target2 = sol2[-1]
path2 = find_path(board2, target2)
print('Legal Path:', path2)

# Unsuccessful Test Case 3: Generate 8x8 board with no legal solution
# first creating the 8x8 board with 5 legal steps solution
board3, sol3 = create_game(8, 5)
# randomly changing the target cell and hoping it is not reachable from the start cell
target3 = (8,8)
path3 = find_path(board3, target3)
print('However, I have changed the target cell to fail the test case')
print('Legal Path:', path3)