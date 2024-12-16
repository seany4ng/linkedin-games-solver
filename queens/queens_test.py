from queens import Board, INT_TO_VALUE_TYPE, VALUE_TYPE_TO_INT

def test_board_110():
    """
    Queens no. 110.
    Source: https://www.linkedin.com/posts/queens-game_queens-no-110-activity-7230830794267635712-QCvO?utm_source=share&utm_medium=member_desktop
    """
    # Recall: 1 -> n for each color
    board = [
        [1, 1, 2, 2, 2, 3, 3, 3, 3],
        [1, 1, 2, 4, 5, 3, 3, 3, 3],
        [1, 1, 4, 4, 5, 6, 6, 3, 3],
        [1, 1, 4, 5, 5, 5, 6, 6, 3],
        [1, 5, 5 ,5, 5, 5, 5, 5, 7],
        [1, 8, 8, 5, 5, 5, 9, 7, 7],
        [1, 7, 8, 8, 5, 9, 9, 7, 7],
        [7, 7, 7, 7, 5, 9, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7]
    ]

    # Act
    board_class = Board(
        board_size = len(board),
        board = board
    )
    board_class.solve_board()

    # Assert
    solved_soln_110 = (
        # 2d array with all 0s except for 1s in column 5, 9, 7, 3, 8, 1, 4, 6, 2 respectively
        [
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0]
        ]
    )
    expected_soln_110 = [[INT_TO_VALUE_TYPE[x] for x in row] for row in solved_soln_110]
    print([[VALUE_TYPE_TO_INT[x] for x in row] for row in board_class.solution])
    assert board_class.solution == expected_soln_110

    print("Test Queens 110 Complete!")

def test_board_229():
    """
    Queens no. 229.
    Source: https://www.linkedin.com/showcase/queens-game/posts/?feedView=all
    """
    # Recall: 1 -> n for each color
    board = [
        [1, 1, 2, 2, 2, 3, 3, 3, 3],
        [1, 4, 4, 4, 2, 3, 2, 5, 3],
        [1, 1, 1, 4, 2, 2, 2, 5, 3],
        [6, 7, 7, 4, 4, 4, 8, 5, 3],
        [6, 7, 9, 9, 9, 4, 8, 5, 3],
        [6, 7, 9, 8, 4, 4, 8, 5, 3],
        [6, 7, 9, 8, 8, 8, 8, 5, 3],
        [5, 7, 5, 5, 5, 5, 5, 5, 3],
        [5, 5, 5, 3, 3, 3, 3, 3, 3]
    ]

    # Act
    board_class = Board(
        board_size = len(board),
        board = board
    )
    board_class.solve_board()

    # Assert
    solved_soln_229 = (
        # 2d array with all 0s except for 1s in column 5, 9, 7, 3, 8, 1, 4, 6, 2 respectively
        [
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]
    )
    expected_soln_229 = [[INT_TO_VALUE_TYPE[x] for x in row] for row in solved_soln_229]
    print([[VALUE_TYPE_TO_INT[x] for x in row] for row in board_class.solution])
    assert board_class.solution == expected_soln_229

    print("Test Queens 229 Complete!")

test_board_110()
test_board_229()
