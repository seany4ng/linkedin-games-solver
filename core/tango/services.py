from core.tango.tango_board import TangoBoard, BoardValueEnum, EqOrDiff


def convert_solved_board_to_string(
    solved_board: list[list[BoardValueEnum]],
) -> list[list[str]]:
    return ([
        [
            " " if val == BoardValueEnum.BLANK else (
                "O" if val == BoardValueEnum.SUN else "X"
            ) for val in row
        ] for row in solved_board
    ])


def solve_tango_board(
    board: list[list[str]],
    vertical_lines: list[list[str]],
    horizontal_lines: list[list[str]],
) -> list[list[str]]:
    eqs: list[EqOrDiff] = []
    diffs: list[EqOrDiff] = []
    for i in range(len(vertical_lines)):
        for j in range(len(vertical_lines)):
            if vertical_lines[i][j] == "=":
                eqs.append(
                    EqOrDiff(
                        is_eq=True,
                        is_row=True,
                        row=i,
                        col=j,
                    )
                )

            elif vertical_lines[i][j] == "x":
                diffs.append(
                    EqOrDiff(
                        is_eq=False,
                        is_row=True,
                        row=i,
                        col=j,
                    )
                )

    for i in range(len(horizontal_lines)):
        for j in range(len(horizontal_lines)):
            if horizontal_lines[i][j] == "=":
                eqs.append(
                    EqOrDiff(
                        is_eq=True,
                        is_row=False,
                        row=i,
                        col=j,
                    )
                )

            if horizontal_lines[i][j] == "x":
                diffs.append(
                    EqOrDiff(
                        is_eq=False,
                        is_row=False,
                        row=i,
                        col=j,
                    )
                )

    tango_board = TangoBoard(
        board=board,
        eqs=eqs,
        diffs=diffs,
    )
    response = tango_board.solve_board()
    if response is None:
        return convert_solved_board_to_string(
            solved_board=tango_board.board,
        )
    
    # TODO: figure out a way to propagate the error string from solve_board()
    return [[]]
