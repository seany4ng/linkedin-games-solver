from typing import Any
from core.app.exceptions import APIException
from core.tango.tango_board import BoardValueEnum, BOARD_SIZE, EqOrDiff, TangoBoard, VALUE_TO_STR_TYPE


import copy, random


def is_valid_board(board: list[list[str]]) -> bool:
    if len(board) != BOARD_SIZE or len(board[0]) != BOARD_SIZE:
        return False
    
    for row in board:
        if not TangoBoard.is_line_correct(row):
            return False
        
    for col in zip(*board):
        if not TangoBoard.is_line_correct(col):
            return False
        
    return True


def try_generate_random_tango_board() -> list[list[BoardValueEnum]] | None:
    """
    Attempts to generate a fully randomized Tango board filled with suns and moons.
    Uses previously generated columns to dictate future rows.
    If at some point the generation becomes impossible, we fail and return None.
    """
    board = []
    for i in range(BOARD_SIZE):
        new_row = [BoardValueEnum.BLANK for i in range(BOARD_SIZE)]
        # First, fill in column obligations
        for j, col in enumerate(zip(*board)):
            # Handle case of avoiding 3 in a row first
            if len(col) > 2 and col[-1] == col[-2]:
                new_row[j] = TangoBoard.get_opposite_value(col[-1])

            # Next, handle cases of potentially having 3 in a row already.
            sun_count, moon_count = col.count(BoardValueEnum.SUN), col.count(BoardValueEnum.MOON)
            if sun_count == 3:
                new_row[j] = BoardValueEnum.MOON

            if moon_count == 3:
                new_row[j] = BoardValueEnum.SUN

        # Then, interpolate rows.
        for i in range(BOARD_SIZE - 1):
            if [BoardValueEnum.MOON] * 2 == new_row[i : i + 2]:
                # Fill edges with sun
                if i - 1 >= 0:
                    new_row[i - 1] = BoardValueEnum.SUN

                if i + 2 < BOARD_SIZE:
                    new_row[i + 2] = BoardValueEnum.SUN

            if [BoardValueEnum.SUN] * 2 == new_row[i : i + 2]:
                # Fill edges with moon
                if i - 1 >= 0:
                    new_row[i - 1] = BoardValueEnum.MOON

                if i + 2 < BOARD_SIZE:
                    new_row[i + 2] = BoardValueEnum.MOON

        # We have now abided by column rules, as well as row-based rules.
        # For the remaining values, we will fill them in using a random permutation
        # of the number of moons/suns left, permuting until we reach a satisfactory solution.
        # If the number of iterations to reach a satisfactory solution becomes too high, we will return None.
        moons_left = (BOARD_SIZE // 2) - new_row.count(BoardValueEnum.MOON)
        suns_left = (BOARD_SIZE // 2) - new_row.count(BoardValueEnum.SUN)
        remaining = [BoardValueEnum.MOON] * moons_left + [BoardValueEnum.SUN] * suns_left
        three_moons = [BoardValueEnum.MOON] * 3
        three_suns = [BoardValueEnum.SUN] * 3
        has_three = True
        num_iters = 0
        while has_three:
            random.shuffle(remaining)
            remaining_index = 0
            for new_row_index in range(BOARD_SIZE):
                if new_row[new_row_index] == BoardValueEnum.BLANK:
                    new_row[new_row_index] = remaining[remaining_index]
                    remaining_index += 1

            # Check now if we have a working solution
            has_three = False
            for i in range(BOARD_SIZE - 2):
                if three_moons == new_row[i : i + 3] or three_suns == new_row[i : i + 3]:
                    has_three = True

            num_iters += 1
            if num_iters > 10:
                return None
            
        board.append(new_row)

    return board


def generate_random_tango_board(
    num_eqs_or_diff: int,
) -> tuple[
    list[list[str]],
    list[list[str]],
    list[list[str]],
    list[list[str]],
]:
    """
    Generates a random, unsolved tango Board.
    Returns:
        board: a blank board
        diffs: the diffs required
        eqs: the eqs required
        solution: the board representing the intended solution
    """
    generated_board = try_generate_random_tango_board()
    while generated_board is None or not is_valid_board(generated_board):
        generated_board = try_generate_random_tango_board()

    # Given the generated board, let's generate a solution.
    # Step 1: Randomly pick a bunch of eq and diff.
    eqs: list[Any] = []
    diffs: list[Any] = []
    used_rows = set()
    used_cols = set()
    for i in range(num_eqs_or_diff):
        bad = True
        # Find a row/col/is_row that hasn't been used (for the same type).
        while bad:
            bad = False
            is_row = random.random() > 0.5
            ind = random.randint(0, 29)
            bigger = ind % 6
            smaller = ind // 6
            if is_row:
                row, col = bigger, smaller
                next_row, next_col = row, col + 1
                if (row, col) in used_rows:
                    bad = True
                used_rows.add((row, col))
            else:
                row, col = smaller, bigger
                next_row, next_col = row + 1, col
                if (row, col) in used_cols:
                    bad = True
                used_cols.add((row, col))

        # If they match, it's an eq; otherwise it's a diff.
        if generated_board[row][col] == generated_board[next_row][next_col]:
            eqs.append(
                EqOrDiff(
                    is_eq=True,
                    is_row=is_row,
                    row=row,
                    col=col,
                )
            )
        else:
            diffs.append(
                EqOrDiff(
                    is_eq=False,
                    is_row=is_row,
                    row=row,
                    col=col,
                )
            )
            
    # Next, let's create a set of the remaining non-blank elements.
    filled_squares = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if generated_board[i][j] != BoardValueEnum.BLANK:
                filled_squares.add((i, j))

    prev_solution = copy.deepcopy(generated_board)

    # ---------------------------------------------------------------------------------
    # CHANGED SECTION: Instead of immediately breaking on the first failure,
    # we revert the tile removal that caused unsolvability and try removing another tile.
    # Once we've exhausted all squares, if we never remove anything else successfully,
    # we end the process.
    # ---------------------------------------------------------------------------------
    while True:
        found_tile_to_remove = False
        tiles_to_consider = list(filled_squares)
        random.shuffle(tiles_to_consider)

        for x, y in tiles_to_consider:
            new_solution = copy.deepcopy(prev_solution)
            new_solution[x][y] = BoardValueEnum.BLANK

            # Try solving the board with that tile removed
            new_board = TangoBoard(
                board=[[VALUE_TO_STR_TYPE[val] for val in row] for row in new_solution],
                diffs=diffs,
                eqs=eqs,
            )

            try:
                new_board.solve_board()
                # If it solves successfully, keep the tile removed
                filled_squares.remove((x, y))
                prev_solution = new_solution
                found_tile_to_remove = True
                # Break to re-shuffle and see if there's still more we can remove
                break
            except APIException:
                # If it fails, revert and try the next tile
                pass

        # If we didn't manage to remove any tile in this iteration,
        # then we are done removing tiles altogether
        if not found_tile_to_remove:
            break
    # ---------------------------------------------------------------------------------

    # Now, we have a blank Tango board and an expected solution. Return it.
    return (
        [[VALUE_TO_STR_TYPE[x] for x in row] for row in prev_solution],  # blank board
        eqs,
        diffs,
        generated_board,  # the intended solution
    )


def convert_eqs_diffs_to_str(
    eqs: list[EqOrDiff],
    diffs: list[EqOrDiff],
) -> tuple[list[list[str]], list[list[str]]]:
    row_lines = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    col_lines = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    eqs_and_diffs = eqs + diffs
    for eq_or_diff in eqs_and_diffs:
        if eq_or_diff.is_row:
            row_lines[eq_or_diff.row][eq_or_diff.col] = "=" if eq_or_diff.is_eq else "x"
        else:
            col_lines[eq_or_diff.row][eq_or_diff.col] = "=" if eq_or_diff.is_eq else "x"

    return row_lines, col_lines