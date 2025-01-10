from typing import Any
from core.app.exceptions import APIException
from core.queens.queens_board import QueensBoard, QueensBoardInsufficientException

import copy, random
import os

def solve_n_queens(n: int) -> list[int]:
    """
    Generates random n_queens solution given n
    """
    with open("core/queens/n_queens/" + str(n) + "_queens_solutions.txt", "r") as f:
        lines = f.readlines()
        random_line = random.choice(lines).strip()
        return list(map(int, random_line.split()))

def try_generate_random_queens_board(n: int) -> tuple[list[int], list[list[int]]]:
    
    n_queens_board = solve_n_queens(n)
    board = [[0 for _ in range(n)] for _ in range(n)]

    color_locations = list(range(1, n + 1))
    random.shuffle(color_locations)
    for i, col in enumerate(n_queens_board):
        board[i][col] = color_locations.pop()

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

    return n_queens_board, board

def generate_random_queens_board(n: int) -> tuple[int, list[list[int]], list[int]]:

    generated_solution, generated_board = try_generate_random_queens_board(n)

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
            generated_solution, generated_board = try_generate_random_queens_board(n)
    
    return num_generated, generated_board, generated_solution