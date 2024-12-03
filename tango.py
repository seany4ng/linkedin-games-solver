from typing import Any
from enum import Enum


class BoardValueEnum(Enum):
    BLANK = 0
    SUN = 1
    MOON = 2


class RuleEnum(Enum):
    SOLVE_ROW = 0
    SOLVE_COL = 1
    SOLVE_EDGE_FROM_EQ = 2
    SOLVE_EQ_FROM_EDGE = 3
    # TODO: add more rules


# A board size of n indicates an n x n tango board.
BOARD_SIZE = 6

# A mapping from integer inputs to an enum value.
INT_TO_VALUE_TYPE = {
    0: BoardValueEnum.BLANK,
    1: BoardValueEnum.SUN,
    2: BoardValueEnum.MOON,
}


class Board:
    def __init__(self, board: list[list[int]], diffs: list[Any], eqs: list[Any]):
        if len(board) != BOARD_SIZE or len(board[0]) != BOARD_SIZE:
            raise ValueError("Invalid board inputted")
        
        self.board = [[INT_TO_VALUE_TYPE[x] for x in board[i]] for i in range(len(board))]
        self.diffs = diffs # Indicates any x on the board
        self.eqs = eqs # Indicates any = on the board
        self.backtrack_stack = [] # Used for backtracking


    def solve_board(self):
        while True:
            # Save the prev board state to compare for back-tracking
            prev_board_state = self.board
            for rule in RuleEnum:
                match rule:
                    case RuleEnum.SOLVE_ROW:
                        pass
                    case RuleEnum.SOLVE_COL:
                        pass
                    case RuleEnum.SOLVE_EDGE_FROM_EQ:
                        pass
                    case RuleEnum.SOLVE_EQ_FROM_EDGE:
                        pass

            # Compare the old board to the new board. if it's equal, we need to backtrack
            if prev_board_state == self.board:
                # TODO: backtrack.
                pass