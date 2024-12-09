from core.tango import Board, BOARD_SIZE, INT_TO_VALUE_TYPE, EqOrDiff


def test_board_57():
    """
    Tango no. 57.
    Source: https://www.linkedin.com/posts/tango-game_tango-no-57-activity-7269621400477327361-NWjE
    """
    # Recall: 0 -> Blank; 1 -> Sun; 2 -> Moon.
    # Arrange
    board = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    board[0][0] = "O"
    board[0][1] = "O"
    board[1][0] = "O"
    board[1][1] = "O"

    # All = signs on the board
    eqs = []
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=True,
            row=2,
            col=2,
        )
    )
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=False,
            row=2,
            col=2,
        )
    )
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=False,
            row=2,
            col=3,
        )
    )
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=True,
            row=3,
            col=2,
        )
    )

    # All x on the board
    diffs = []
    diffs.append(
        EqOrDiff(
            is_eq=False,
            is_row=True,
            row=4,
            col=4,
        )
    )
    diffs.append(
        EqOrDiff(
            is_eq=False,
            is_row=False,
            row=4,
            col=4,
        )
    )
    diffs.append(
        EqOrDiff(
            is_eq=False,
            is_row=True,
            row=5,
            col=4,
        )
    )
    diffs.append(
        EqOrDiff(
            is_eq=False,
            is_row=False,
            row=4,
            col=5,
        )
    )

    # Act
    board_class = Board(
        board=board,
        diffs=diffs,
        eqs=eqs,
    )
    board_class.solve_board()

    # Assert
    solved_board_0 = (
        [
            [1, 1, 2, 2, 1, 2],
            [1, 1, 2, 2, 1, 2],
            [2, 2, 1, 1, 2, 1],
            [2, 2, 1, 1, 2, 1],
            [1, 1, 2, 2, 1, 2],
            [2, 2, 1, 1, 2, 1],
        ]
    )
    expected_board_0 = [[INT_TO_VALUE_TYPE[x] for x in row] for row in solved_board_0]
    assert board_class.board == expected_board_0

    print("Test Tango 57 Complete!")

    

def test_board_55():
    """
    Tango no. 55.
    Source: https://www.linkedin.com/posts/tango-game_tango-no-55-activity-7268896609373949952-gW07
    """
    # Recall: 0 -> Blank; 1 -> Sun; 2 -> Moon.
    # Arrange
    board = [[" " for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    board[0][0] = "X"
    board[4][5] = "O"
    board[5][4] = "O"
    board[5][5] = "X"

    # All = signs on the board
    eqs = []
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=True,
            row=0,
            col=4,
        )
    )
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=False,
            row=0,
            col=5,
        )
    )
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=False,
            row=4,
            col=0,
        )
    )
    eqs.append(
        EqOrDiff(
            is_eq=True,
            is_row=True,
            row=5,
            col=0,
        )
    )

    # All x on the board
    diffs = []
    diffs.append(
        EqOrDiff(
            is_eq=False,
            is_row=False,
            row=0,
            col=1,
        )
    )
    diffs.append(
        EqOrDiff(
            is_eq=False,
            is_row=True,
            row=1,
            col=0,
        )
    )

    # Act
    board_class = Board(
        board=board,
        diffs=diffs,
        eqs=eqs,
    )
    board_class.solve_board()

    # Assert
    solved_board_1 = (
        [
            [2, 2, 1, 2, 1, 1],
            [2, 1, 2, 1, 2, 1],
            [1, 2, 1, 1, 2, 2],
            [2, 1, 1, 2, 1, 2],
            [1, 2, 2, 1, 2, 1],
            [1, 1, 2, 2, 1, 2],
        ]
    )
    expected_board_1 = [[INT_TO_VALUE_TYPE[x] for x in row] for row in solved_board_1]
    assert board_class.board == expected_board_1

    print("Test Tango 55 Complete!")


# BEGIN: RUN TESTS 
test_board_57()
test_board_55()

# END: RUN TESTS
