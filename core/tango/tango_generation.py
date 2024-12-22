from typing import Any
from core.tango.tango_board import BoardValueEnum, BOARD_SIZE, TangoBoard, VALUE_TO_STR_TYPE


import random


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
        # if the number of iterations to reach a satisfactory solution becomes too high, we will return None.
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


def generate_random_tango_board() -> list[list[str]]:
    """
    Tries generating a Tango board until a valid one is generated.
    Due to randomness, this may require calling our generation function multiple times.
    Using basic counting, we can show that the probability that an invalid board is generated
    is 0.3, or 6/20. The computation is left as an exercise to the user.
    """
    generated_board = try_generate_random_tango_board()
    while generated_board is None or not is_valid_board(generated_board):
        generated_board = try_generate_random_tango_board()

    # Returns a 2d list of strings
    return [[VALUE_TO_STR_TYPE[x] for x in row] for row in generated_board]
