#!/usr/bin/env python3
"""
Backtracking Sudoku Solver
"""

def sudoku_solver(grid):
    row,col = find_emtpy(grid)
    if (row == None):
        return True

    for num in range(1,10):
        if (check_feasible(grid, row, col, num)):
            grid[row][col] = num;
            if (sudoku_solver(grid)):
                return True
            grid[row][col] = 0
    return False


def find_emtpy(grid):
    n = len(grid)
    for row in range(n):
        for col in range(n):
            if (grid[row][col] == 0):
                return row,col
    return None,None


def already_in_row(grid, row, num):
    n = len(grid)
    for col in range(n):
        if (grid[row][col] == num):
            return True
    return False


def already_in_col(grid, col, num):
    n = len(grid)
    for row in range(n):
        if (grid[row][col] == num):
            return True
    return False


def already_in_box(grid, box_offset_row, box_offset_col, num):
    for row in range(3):
        for col in range(3):
            if (grid[row+box_offset_row][col+box_offset_col] == num):
                return True
    return False


def check_feasible(grid, row, col, num):
    return (not already_in_row(grid, row, num) and \
            not already_in_col(grid, col, num) and \
            not already_in_box(grid, row - row%3 , col - col%3, num))


def print_grid(grid):
    n = len(grid)
    for row_ind, row in enumerate(grid):
        if row_ind % 3 == 0:
            print("-----------------------------")
        for col_ind, val in enumerate(row):
            if col_ind == 8:
                print(" ", val, "|")
            elif col_ind % 3 == 0:
                print("|", val, end="")
            else:
                print(" ", val, end="")
    print("-----------------------------")


def main():
    grid = [[0, 0, 0, 2, 0, 0, 0, 0, 1],
            [8, 2, 0, 0, 0, 0, 0, 5, 0],
            [0, 0, 0, 0, 9, 5, 0, 4, 0],
            [0, 0, 2, 0, 0, 3, 0, 0, 9],
            [0, 0, 1, 0, 8, 0, 2, 0, 0],
            [5, 0, 0, 1, 0, 0, 3, 0, 0], 
            [0, 7, 0, 3, 6, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 9, 6],
            [4, 0, 0, 0, 0, 2, 0, 0, 0],
    ]
    print_grid(grid)
    if sudoku_solver(grid):
        print_grid(grid)
    else:
        print("No solution exists.")

if __name__ == '__main__':
    main()

"""
    #easy
    grid = [[0, 0, 8, 9, 3, 0, 0, 1, 0],
            [0, 0, 5, 0, 0, 6, 3, 7, 0],
            [3, 7, 0, 0, 2, 5, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 6, 0],
            [9, 2, 1, 4, 0, 3, 8, 5, 7],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 5, 9, 0, 0, 4, 8],
            [0, 9, 2, 6, 0, 0, 5, 0, 0],
            [0, 5, 0, 0, 1, 4, 9, 0, 0]
    ]
    
    # medium
    grid = [[0, 0, 0, 1, 0, 0, 5, 4, 0],
            [7, 1, 0, 3, 0, 0, 0, 9, 0],
            [5, 0, 3, 2, 9, 0, 0, 0, 0],
            [2, 7, 0, 5, 0, 0, 0, 6, 0],
            [0, 0, 5, 0, 0, 0, 4, 0, 0],
            [0, 9, 0, 0, 0, 4, 0, 2, 5],
            [0, 0, 0, 0, 3, 6, 9, 0, 7],
            [0, 5, 0, 0, 0, 2, 0, 3, 4],
            [0, 6, 7, 0, 0, 9, 0, 0, 0]
    ]
    
    # hard
    grid = [[0, 1, 0, 0, 0, 2, 6, 0, 0],
            [0, 0, 0, 0, 0, 8, 7, 0, 0],
            [0, 0, 2, 0, 1, 9, 0, 8, 0],
            [1, 0, 9, 0, 0, 7, 0, 4, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 7, 0, 4, 0, 0, 1, 0, 5],
            [0, 9, 0, 2, 3, 0, 4, 0, 0],
            [0, 0, 1, 8, 0, 0, 0, 0, 0],
            [0, 0, 6, 9, 0, 0, 0, 1, 0],
    ]
    
    # evil
    grid = [[0, 0, 0, 2, 0, 0, 0, 0, 1],
            [8, 2, 0, 0, 0, 0, 0, 5, 0],
            [0, 0, 0, 0, 9, 5, 0, 4, 0],
            [0, 0, 2, 0, 0, 3, 0, 0, 9],
            [0, 0, 1, 0, 8, 0, 2, 0, 0],
            [5, 0, 0, 1, 0, 0, 3, 0, 0], 
            [0, 7, 0, 3, 6, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 9, 6],
            [4, 0, 0, 0, 0, 2, 0, 0, 0],
    ]
"""