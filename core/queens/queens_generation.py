from typing import Any
from core.app.exceptions import APIException
from core.queens.queens_board import QueensBoard, QueensBoardInsufficientException

import copy, random

def solve_n_queens(n: int) -> list[list[int]]:
    """
    Solve the n-Queens problem via backtracking.
    Returns a list 'cols' of length n, where cols[row] = column index
    of the queen in that row.
    """
    cols = [-1] * n  # cols[i] = column of queen in row i

    def is_safe(row, col):
        for r in range(row):
            c = cols[r]
            if c == col:  # same column
                return False
            if abs(r - row) == abs(c - col):  # same diagonal
                return False
        return True

    def backtrack(row):
        if row == n:
            return True
        for col in range(n):
            if is_safe(row, col):
                cols[row] = col
                if backtrack(row + 1):
                    return True
                cols[row] = -1
        return False

    backtrack(0)
    return cols

def try_generate_random_queens_board(n: int) -> list[list[int]]:
    
    n_queens_board = solve_n_queens(n)
    board = [[0 for _ in range(n)] for _ in range(n)]
    for i, col in enumerate(n_queens_board):
        board[i][col] = i + 1

    rows, cols = len(board), len(board[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and board[x][y] == 0

    def flood_once(x, y, value):
        random.shuffle(directions)  # Randomize directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                board[nx][ny] = value
                return nx, ny
        return None, None

    non_zero_cells = [(x, y) for x in range(rows) for y in range(cols) if board[x][y] != 0]

    while any(0 in row for row in board):
        x, y = random.choice(non_zero_cells)
        value = board[x][y]
        nx, ny = flood_once(x, y, value)
        if nx is not None and ny is not None:
            non_zero_cells.append((nx, ny))

    return board

def generate_random_queens_board(n: int) -> tuple[int, list[list[int]]]:

    generated_board = try_generate_random_queens_board(n)

    # Try solving the board, if it fails, try generating a new board
    # and solving it, repeat until a solution is found.
    num_generated = 0
    while True:
        try:
            test_board = QueensBoard(
                board_size = n,
                board=generated_board,
            )
            test_board.solve_board()
            num_generated += 1
            break
        except QueensBoardInsufficientException:
            generated_board = try_generate_random_queens_board(n)
    
    return num_generated, generated_board