from typing import Any
from enum import Enum
from dataclasses import dataclass


class BoardValueEnum(Enum):
    BLANK = 0
    SUN = 1
    MOON = 2


class RuleEnum(Enum):
    SOLVE_EQ_DIFF = 0
    SOLVE_ROW = 1
    SOLVE_COL = 2
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
                    case RuleEnum.SOLVE_EQ_DIFF:
                        self.solve_eq_diff()
                    case RuleEnum.SOLVE_ROW:
                        self.solve_row_rule()
                    case RuleEnum.SOLVE_COL:
                        self.solve_col_rule()
                    case RuleEnum.SOLVE_EQ_FROM_EDGE:
                        self.solve_eq_from_edge()

            # Compare the old board to the new board. if it's equal, we need to backtrack
            if prev_board_state == self.board:
                # TODO: backtrack.
                pass


    def get_opposite_value(self, value: BoardValueEnum) -> BoardValueEnum:
        """Returns the opposite value of a board value"""
        if value == BoardValueEnum.SUN:
            return BoardValueEnum.MOON
        elif value == BoardValueEnum.MOON:
            return BoardValueEnum.SUN
        return BoardValueEnum.BLANK


    def fill_eq_diff(self, symbol: Any, isEq: bool):
        """Fills in opposing side of = or x"""
        x1, y1, x2, y2 = symbol.row, symbol.col, symbol.row + (0 if symbol.is_row else 1), symbol.col + (1 if symbol.is_row else 0)
        tile1, tile2 = self.board[x1][y1], self.board[x2][y2]

        if tile1 != BoardValueEnum.BLANK and tile2 == BoardValueEnum.BLANK:
            self.board[x2][y2] = tile1 if isEq else self.get_opposite_value(tile1)
        elif tile2 != BoardValueEnum.BLANK and tile1 == BoardValueEnum.BLANK:
            self.board[x1][y1] = tile2 if isEq else self.get_opposite_value(tile2)


    def solve_eq_diff(self):
        """Solves = or x if one is filled"""
        # RULE = : fill other side of = with matching element
        for symbol in self.eqs:
            self.fill_eq_diff(symbol, True)

        # RULE x : fill other side of x with opposite element
        for symbol in self.diffs:
            self.fill_eq_diff(symbol, False)


    def solve_rule(self, board: list[list[BoardValueEnum]]):
        """Attempts to solve a row, for all possible rows"""
        # RULE 1: If 3 moons/suns in a row/col, fill remainder with opposite
        for idx, line in enumerate(board):
            sun_count = line.count(BoardValueEnum.SUN)
            moon_count = line.count(BoardValueEnum.MOON)
            if sun_count == 3:
                board[idx] = [BoardValueEnum.MOON if x == BoardValueEnum.BLANK else x for x in line]
            if moon_count == 3:
                board[idx] = [BoardValueEnum.SUN if x == BoardValueEnum.BLANK else x for x in line]

        # RULE 2: If 2 moons/suns in a row/col, fill edges with opposite
        for idx, line in enumerate(board):
            for i in range(len(line) - 2):
                if line[i] == BoardValueEnum.MOON and line[i+1] == BoardValueEnum.MOON and line[i+2] == BoardValueEnum.BLANK:
                    board[idx][i+2] = BoardValueEnum.SUN
                if line[i] == BoardValueEnum.BLANK and line[i+1] == BoardValueEnum.MOON and line[i+2] == BoardValueEnum.MOON:
                    board[idx][i] = BoardValueEnum.SUN

                if line[i] == BoardValueEnum.SUN and line[i+1] == BoardValueEnum.SUN and line[i+2] == BoardValueEnum.BLANK:
                    board[idx][i+2] = BoardValueEnum.MOON
                if line[i] == BoardValueEnum.BLANK and line[i+1] == BoardValueEnum.SUN and line[i+2] == BoardValueEnum.SUN:
                    board[idx][i] = BoardValueEnum.MOON


    def solve_row_rule(self):
        """For each row, try to solve it using Tango's 3-3 rule"""
        self.solve_rule(self.board)


    def solve_col_rule(self):
        """For each col, try to solve it using Tango's 3-3 rule"""
        transposed_board = [list(col) for col in zip(*self.board)]
        self.solve_rule(transposed_board)
        self.board = [list(row) for row in zip(*transposed_board)]


    def solve_eq_from_edge(self):
        """Given a solved board value on the edge of a =, solve the ="""
        # RULE 3: If empty eq, value must be opposite to edge
        for eq in self.eqs: 
            x1, y1, x2, y2 = x1, y1, x2, y2 = eq.row, eq.col, eq.row + (0 if eq.is_row else 1), eq.col + (1 if eq.is_row else 0)
            if self.board[x1][y1] == self.board[x2][y2] == BoardValueEnum.BLANK:
                if eq.is_row:
                    left, right = y1 - 1, y2 + 1
                    if left >= 0:
                        self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(self.board[x1][left])
                    elif right < BOARD_SIZE:
                        self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(self.board[x1][right])
                else:
                    top, bottom = x1 - 1, x2 + 1
                    if top >= 0:
                        self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(self.board[top][y1])
                    elif bottom < BOARD_SIZE:
                        self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(self.board[bottom][y1])


    def perform_backtrack(self):
        pass
