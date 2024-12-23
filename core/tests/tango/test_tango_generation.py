from core.tango.tango_board import INT_TO_VALUE_TYPE, TangoBoard
from core.tango.tango_generation import generate_random_tango_board


def test_try_generate_board():
    """
    Try generating a Tango board 100 times.
    """
    (
        generated_board,
        diffs,
        eqs,
        solution,
    ) = generate_random_tango_board(8)
    new_tango_board = TangoBoard(
        board=generated_board,
        diffs=diffs,
        eqs=eqs,
    )
    print("Printing randomly generated board before solving:")
    new_tango_board.print_board()
    new_tango_board.solve_board()
    assert new_tango_board.board == solution
