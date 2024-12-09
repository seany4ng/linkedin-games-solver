from core.tango import (
    BOARD_SIZE,
    INT_TO_VALUE_TYPE,
    STR_TO_VALUE_TYPE,
    Board,
    EqOrDiff,
)
from core.services import solve_tango_board


def test_solve_tango_board_57():
    """
    Tango no. 57.
    Source: https://www.linkedin.com/posts/tango-game_tango-no-57-activity-7269621400477327361-NWjE
    This tests if the service function performs the solve
    """
    # Arrange
    board = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    board[0][0] = "O"
    board[0][1] = "O"
    board[1][0] = "O"
    board[1][1] = "O"
    vertical_lines = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    horizontal_lines = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    vertical_lines[2][2] = "="
    vertical_lines[3][2] = "="
    vertical_lines[4][4] = "x"
    vertical_lines[5][4] = "x"

    horizontal_lines[2][2] = "="
    horizontal_lines[2][3] = "="
    horizontal_lines[4][4] = "x"
    horizontal_lines[4][5] = "x"

    # Act
    actual_board = solve_tango_board(
        board=board,
        vertical_lines=vertical_lines,
        horizontal_lines=horizontal_lines,
    )

    # Assert
    expected_board = (
        [
            ["O", "O", "X", "X", "O", "X"],
            ["O", "O", "X", "X", "O", "X"],
            ["X", "X", "O", "O", "X", "O"],
            ["X", "X", "O", "O", "X", "O"],
            ["O", "O", "X", "X", "O", "X"],
            ["X", "X", "O", "O", "X", "O"],
        ]
    )
    assert expected_board == actual_board
    print("test_solve_tango_board_57 Complete!")


# BEGIN: RUN TESTS
test_solve_tango_board_57()

# END: RUN TESTS
