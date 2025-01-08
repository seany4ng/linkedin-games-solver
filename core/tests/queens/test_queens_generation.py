from core.queens.queens_board import QueensBoard
from core.queens.queens_generation import generate_random_queens_board


def test_try_generate_board():
    """
    Try generating a Queens board 100 times.
    """
    (
        num_generated,
        generated_board,
    ) = generate_random_queens_board(8)

    new_queens_board = QueensBoard(
        board_size = 8,
        board=generated_board,
    )
    new_queens_board.solve_board()
    assert new_queens_board.solved_board_is_correct()
