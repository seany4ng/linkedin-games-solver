from queens import Board, INT_TO_VALUE_TYPE, VALUE_TYPE_TO_INT

def test_board_110():
    """
    Queens no. 110.
    Source: https://www.linkedin.com/posts/tango-game_tango-no-57-activity-7269621400477327361-NWjE
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

    

# def test_board_55():
#     """
#     Tango no. 55.
#     Source: https://www.linkedin.com/posts/tango-game_tango-no-55-activity-7268896609373949952-gW07
#     """
#     # Recall: 0 -> Blank; 1 -> Sun; 2 -> Moon.
#     # Arrange
#     board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
#     board[0][0] = 2
#     board[4][5] = 1
#     board[5][4] = 1
#     board[5][5] = 2

#     # All = signs on the board
#     eqs = []
#     eqs.append(
#         EqOrDiff(
#             is_eq=True,
#             is_row=True,
#             row=0,
#             col=4,
#         )
#     )
#     eqs.append(
#         EqOrDiff(
#             is_eq=True,
#             is_row=False,
#             row=0,
#             col=5,
#         )
#     )
#     eqs.append(
#         EqOrDiff(
#             is_eq=True,
#             is_row=False,
#             row=4,
#             col=0,
#         )
#     )
#     eqs.append(
#         EqOrDiff(
#             is_eq=True,
#             is_row=True,
#             row=5,
#             col=0,
#         )
#     )

#     # All x on the board
#     diffs = []
#     diffs.append(
#         EqOrDiff(
#             is_eq=False,
#             is_row=False,
#             row=0,
#             col=1,
#         )
#     )
#     diffs.append(
#         EqOrDiff(
#             is_eq=False,
#             is_row=True,
#             row=1,
#             col=0,
#         )
#     )

#     # Act
#     board_class = Board(
#         board=board,
#         diffs=diffs,
#         eqs=eqs,
#     )
#     board_class.solve_board()

#     # Assert
#     solved_board_1 = (
#         [
#             [2, 2, 1, 2, 1, 1],
#             [2, 1, 2, 1, 2, 1],
#             [1, 2, 1, 1, 2, 2],
#             [2, 1, 1, 2, 1, 2],
#             [1, 2, 2, 1, 2, 1],
#             [1, 1, 2, 2, 1, 2],
#         ]
#     )
#     expected_board_1 = [[INT_TO_VALUE_TYPE[x] for x in row] for row in solved_board_1]
#     assert board_class.board == expected_board_1

#     print("Test Tango 55 Complete!")

test_board_110()
# test_board_55()
