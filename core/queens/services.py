from core.queens.queens_board import QueensBoard

def solve_queens_board(
    board_size: int,
    board: list[list[int]],
) -> list[list[int]]:
    queens_board = QueensBoard(board)
    queens_board.solve()
    return queens_board.get_board(
        queens_board.get_solved_board()
    
)