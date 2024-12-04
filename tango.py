from typing import Any
from enum import Enum
from dataclasses import dataclass


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


"""
The representation of a "=" or "x" in Tango.
- is_eq: if True, this represents a "=". if False, represents a "x".
- is_row: if True, it represents (row, col), (row + 1, col);
    Otherwise, represents (row, col), (row, col + 1).
- row: the index of the row that the symbol begins at.
- col: the index of the col that the symbol begins at.
"""
@dataclass
class EqOrDiff:
    is_eq: bool
    is_row: bool
    row: int
    col: int


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
                        self.solve_row_rule()
                    case RuleEnum.SOLVE_COL:
                        self.solve_col_rule()
                    case RuleEnum.SOLVE_EDGE_FROM_EQ:
                        pass
                    case RuleEnum.SOLVE_EQ_FROM_EDGE:
                        pass

            # Compare the old board to the new board. if it's equal, we need to backtrack
            if prev_board_state == self.board:
                # TODO: backtrack.
                pass


    def solve_row_rule(self):
        # TODO: function used for SOLVE_ROW rule. add the rule functions below.
        # If it gets to convoluted, we can remove this potentially leaky abstraction.

        # RULE 1: if 3 moons/suns in a row, fill remainder with opposite
        for row_idx, row in enumerate(self.board):
            sun_count = row.count(BoardValueEnum.SUN)
            moon_count = row.count(BoardValueEnum.MOON)
            if sun_count == 3:
                self.board[row_idx] = [BoardValueEnum.MOON if x == BoardValueEnum.BLANK for x in row]
            if moon_count == 3:
                self.board[row_idx] = [BoardValueEnum.SUN if x == BoardValueEnum.BLANK for x in row]

        # RULE 2: if 2 moons/suns in a row, fill edges with opposite
        for row_idx, row in enumerate(self.board):
            for i in range(len(row)-2):
                if row[i] == BoardValueEnum.MOON and row[i+1] == BoardValueEnum.MOON and row[i+2] == BoardValueEnum.BLANK:
                    self.board[row_idx][i+2] = BoardValueEnum.SUN
                if row[i] == BoardValueEnum.BLANK and row[i+1] == BoardValueEnum.MOON and row[i+2] == BoardValueEnum.MOON:
                    self.board[row_idx][i] = BoardValueEnum.SUN

                if row[i] == BoardValueEnum.SUN and row[i+1] == BoardValueEnum.SUN and row[i+2] == BoardValueEnum.BLANK:
                    self.board[row_idx][i+2] = BoardValueEnum.MOON
                if row[i] == BoardValueEnum.BLANK and row[i+1] == BoardValueEnum.SUN and row[i+2] == BoardValueEnum.SUN:
                    self.board[row_idx][i] = BoardValueEnum.MOON
    
    def solve_col_rule(self):

        # Transpose board to work on columns
        transposed_board = list(zip(*self.board))

        # RULE 1: if 3 moons/suns in a col, fill remainder with opposite
        for col_idx, col in enumerate(transposed_board):
            sun_count = col.count(BoardValueEnum.SUN)
            moon_count = col.count(BoardValueEnum.MOON)
            if sun_count == 3:
                transposed_board[col_idx] = [BoardValueEnum.MOON if x == BoardValueEnum.BLANK else x for x in col]
            if moon_count == 3:
                transposed_board[col_idx] = [BoardValueEnum.SUN if x == BoardValueEnum.BLANK else x for x in col]

        # RULE 2: if 2 moons/suns in a row, fill edges with opposite
        for col_idx, col in enumerate(transposed_board):
            for i in range(len(col)-2):
                if col[i] == BoardValueEnum.MOON and col[i+1] == BoardValueEnum.MOON and col[i+2] == BoardValueEnum.BLANK:
                    col[i+2] = BoardValueEnum.SUN
                if col[i] == BoardValueEnum.BLANK and col[i+1] == BoardValueEnum.MOON and col[i+2] == BoardValueEnum.MOON:
                    col[i] = BoardValueEnum.SUN

                if col[i] == BoardValueEnum.SUN and col[i+1] == BoardValueEnum.SUN and col[i+2] == BoardValueEnum.BLANK:
                    col[i+2] = BoardValueEnum.MOON
                if col[i] == BoardValueEnum.BLANK and col[i+1] == BoardValueEnum.SUN and col[i+2] == BoardValueEnum.SUN:
                    col[i] = BoardValueEnum.MOON

        # Transpose back to update the original board
        self.board = [list(row) for row in zip(*transposed_board)]

    def solve_edge_from_eq(self):
        

    def perform_backtrack(self):
        pass