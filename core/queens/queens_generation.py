from typing import Any
from core.app.exceptions import APIException
from core.queens.queens_board import QueensBoard, QueensBoardInsufficientException

import copy, random
import os

def get_random_n_queens(n: int) -> list[int]:
    """
    Generates random n_queens solution given n
    """
    with open("core/queens/n_queens/" + str(n) + "_queens_solutions.txt", "r") as f:
        lines = f.readlines()
        random_line = random.choice(lines).strip()
        return list(map(int, random_line.split()))

def get_random_color_order(n: int) -> list[int]:
    """
    Generates random color order given n
    """
    colors = list(range(1, n + 1))
    random.shuffle(colors)
    return colors

def try_generate_random_queens_board(n: int, board: list[list[int]]) -> list[list[int]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    non_zero_cells = [(x, y) for x in range(n) for y in range(n) if board[x][y] != 0]
    empty_cells = set((x, y) for x in range(n) for y in range(n) if board[x][y] == 0)

    while empty_cells:
        x, y = random.choice(non_zero_cells)
        value = board[x][y]

        # Flood based on least-filled direction
        best_dir = None
        min_neighbors = float('inf')
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in empty_cells:
                neighbors = sum((nx + dx2, ny + dy2) in empty_cells for dx2, dy2 in directions)
                if neighbors < min_neighbors:
                    best_dir = (dx, dy)
                    min_neighbors = neighbors

        if best_dir:
            nx, ny = x + best_dir[0], y + best_dir[1]
            board[nx][ny] = value
            non_zero_cells.append((nx, ny))
            empty_cells.remove((nx, ny))
        else:
            non_zero_cells.remove((x, y))  # If no valid move, remove from pool

    return board


# def try_generate_random_queens_board(n: int, board: list[list[int]]) -> list[list[int]]:
    
#     # board = [[0 for _ in range(n)] for _ in range(n)]

#     # for i, col in enumerate(n_queens_board):
#     #     board[i][col] = color_locations[i]

#     directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

#     def is_valid(x, y):
#         return 0 <= x < n and 0 <= y < n and board[x][y] == 0

#     def flood_once(x, y, value):
#         random.shuffle(directions)  # Randomize directions
#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             if is_valid(nx, ny):
#                 board[nx][ny] = value
#                 return nx, ny
#         return None, None

#     non_zero_cells = [(x, y) for x in range(n) for y in range(n) if board[x][y] != 0]

#     while any(0 in row for row in board):
#         x, y = random.choice(non_zero_cells)
#         value = board[x][y]
#         nx, ny = flood_once(x, y, value)
#         if nx is not None and ny is not None:
#             non_zero_cells.append((nx, ny))

#     return board

def generate_random_queens_board(n: int) -> tuple[int, list[list[int]], list[int]]:

    n_queens_solution = get_random_n_queens(n)
    color_order = get_random_color_order(n)
    board = [[0 for _ in range(n)] for _ in range(n)]
    for i, col in enumerate(n_queens_solution):
        board[i][col] = color_order[i]

    generated_board = try_generate_random_queens_board(n, copy.deepcopy(board))

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
            generated_board = try_generate_random_queens_board(n, copy.deepcopy(board))
    
    return num_generated, generated_board, n_queens_solution