from core.queens.queens_board import QueensBoard, VALUE_TYPE_TO_INT

def solve_queens_board(
    board_size: int,
    board: list[list[int]],
) -> list[list[int]]:
    queens_board = QueensBoard(
        board_size=board_size,
        board=board,
    )
    queens_board.solve_board()
    return [[VALUE_TYPE_TO_INT[x] for x in row] for row in queens_board.solution]