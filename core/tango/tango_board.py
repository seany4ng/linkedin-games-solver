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


# A board size of n indicates an n x n tango board.
BOARD_SIZE = 6

# A mapping from str inputs to an enum value.
STR_TO_VALUE_TYPE = {
    " ": BoardValueEnum.BLANK,
    "O": BoardValueEnum.SUN,
    "X": BoardValueEnum.MOON,
}

# A mapping from int to enum used in testing.
INT_TO_VALUE_TYPE = {
    0: BoardValueEnum.BLANK,
    1: BoardValueEnum.SUN,
    2: BoardValueEnum.MOON,
}


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


class TangoBoard:
    def __init__(self, board: list[list[str]], diffs: list[EqOrDiff], eqs: list[EqOrDiff]):
        if len(board) != BOARD_SIZE or len(board[0]) != BOARD_SIZE:
            raise ValueError("Invalid board inputted")
        self.board = [[STR_TO_VALUE_TYPE[x] for x in row] for row in board]
        self.diffs = diffs # Indicates any x on the board
        self.eqs = eqs # Indicates any = on the board


    def iterate_once(self):
        """Performs one iteration of trying all rules"""
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
    
    
    def solve_board(self):
        while not self.is_solved():
            self.iterate_once()
            # print(self.board)


    ### BEGIN: Rules

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
        for idx, line in enumerate(board):

            # RULE 1: If 3 moons/suns in a row/col, fill remainder with opposite
            sun_count = line.count(BoardValueEnum.SUN)
            moon_count = line.count(BoardValueEnum.MOON)
            if sun_count == 3:
                board[idx] = [BoardValueEnum.MOON if x == BoardValueEnum.BLANK else x for x in line]
            if moon_count == 3:
                board[idx] = [BoardValueEnum.SUN if x == BoardValueEnum.BLANK else x for x in line]

            for i in range(len(line) - 2):

                # RULE 2: If 2 moons/suns in a row/col, fill edges with opposite
                if line[i] == line[i+1] == BoardValueEnum.MOON and line[i+2] == BoardValueEnum.BLANK:
                    board[idx][i+2] = BoardValueEnum.SUN
                if line[i] == BoardValueEnum.BLANK and line[i+1] == line[i+2] == BoardValueEnum.MOON:
                    board[idx][i] = BoardValueEnum.SUN

                if line[i] == line[i+1] == BoardValueEnum.SUN and line[i+2] == BoardValueEnum.BLANK:
                    board[idx][i+2] = BoardValueEnum.MOON
                if line[i] == BoardValueEnum.BLANK and line[i+1] == line[i+2] == BoardValueEnum.SUN:
                    board[idx][i] = BoardValueEnum.MOON

                # RULE 3: If there is a space between 2 moons/suns, fill with opposite
                if line[i] == line[i+2] == BoardValueEnum.MOON and line[i+1] == BoardValueEnum.BLANK:
                    board[idx][i+1] = BoardValueEnum.SUN
                if line[i] == line[i+2] == BoardValueEnum.SUN and line[i+1] == BoardValueEnum.BLANK:
                    board[idx][i+1] = BoardValueEnum.MOON

            
            # RULE 4: If there are moons/suns at both ends, adjacents must be opposites
            if line[0] == line[-1] == BoardValueEnum.MOON:
                line[1] = line[-2] = BoardValueEnum.SUN
            if line[0] == line[-1] == BoardValueEnum.SUN:
                line[1] = line[-2] = BoardValueEnum.MOON

            # RULE 5: If there are 2 moons/suns at an end, opposite end must be opposite
            if line[0] == line[1] == BoardValueEnum.MOON:
                line[-1] = BoardValueEnum.SUN
            if line[-1] == line[-2] == BoardValueEnum.MOON:
                line[0] = BoardValueEnum.SUN
            if line[0] == line[1] == BoardValueEnum.SUN:
                line[-1] = BoardValueEnum.MOON
            if line[-1] == line[-2] == BoardValueEnum.SUN:
                line[0] = BoardValueEnum.MOON
        

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
        for eq in self.eqs: 
            x1, y1, x2, y2 = x1, y1, x2, y2 = eq.row, eq.col, eq.row + (0 if eq.is_row else 1), eq.col + (1 if eq.is_row else 0)
            if self.board[x1][y1] == self.board[x2][y2] == BoardValueEnum.BLANK:

                # RULE 6: If empty eq, eq values must be opposite to edge
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
                

                # RULE 7: If empty eq and 3 values, eq values must be equal to smaller count
                row = self.board[x1] if eq.is_row else [row[y1] for row in self.board]
                sun_count = row.count(BoardValueEnum.SUN)
                moon_count = row.count(BoardValueEnum.MOON)
                if sun_count == 2 and moon_count == 1:
                    self.board[x1][y1] = self.board[x2][y2] = BoardValueEnum.MOON 
                if sun_count == 1 and moon_count == 2:
                    self.board[x1][y1] = self.board[x2][y2] = BoardValueEnum.SUN

                # RULE 8: If empty eq on one end and opposite end filled, eq must be different
                if eq.is_row and y1 == 0 and (grid_val := self.board[x1][-1]) != BoardValueEnum.BLANK:
                    self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(grid_val)
                if eq.is_row and y2 == BOARD_SIZE - 1 and (grid_val := self.board[x1][0]) != BoardValueEnum.BLANK:
                    self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(grid_val)
                if not eq.is_row and x1 == 0 and (grid_val := self.board[-1][y1]) != BoardValueEnum.BLANK:
                    self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(grid_val)
                if not eq.is_row and x2 == BOARD_SIZE - 1 and (grid_val := self.board[0][y1]) != BoardValueEnum.BLANK:
                    self.board[x1][y1] = self.board[x2][y2] = self.get_opposite_value(grid_val)

            # RULE 9: If empty x and 3 values, remaining blank tile must be equal to smaller count
            for diff in self.diffs:
                x1, y1, x2, y2 = diff.row, diff.col, diff.row + (0 if diff.is_row else 1), diff.col + (1 if diff.is_row else 0)
                if self.board[x1][y1] == self.board[x2][y2] == BoardValueEnum.BLANK:
                    row = self.board[x1] if diff.is_row else [row[y1] for row in self.board]
                    sun_count = row.count(BoardValueEnum.SUN)
                    moon_count = row.count(BoardValueEnum.MOON)

                    remaining_blank = next((i for i, value in enumerate(row) if value == BoardValueEnum.BLANK and i not in (y1, y2)), None)

                    if sun_count == 2 and moon_count == 1:
                        if diff.is_row:
                            self.board[x1][remaining_blank] = BoardValueEnum.MOON
                        else:
                            self.board[remaining_blank][y1] = BoardValueEnum.MOON
                    elif sun_count == 1 and moon_count == 2:
                        if diff.is_row:
                            self.board[x1][remaining_blank] = BoardValueEnum.SUN
                        else:
                            self.board[remaining_blank][y1] = BoardValueEnum.SUN



    ### END: Rules

    ### BEGIN: Helpers

    def get_opposite_value(self, value: BoardValueEnum) -> BoardValueEnum:
        """Returns the opposite value of a board value"""
        if value == BoardValueEnum.SUN:
            return BoardValueEnum.MOON
        elif value == BoardValueEnum.MOON:
            return BoardValueEnum.SUN
        return BoardValueEnum.BLANK
    

    def is_solved(self) -> bool:
        """Returns whether the board is fully solved or not"""
        for row in self.board:
            for col in row:
                if col == BoardValueEnum.BLANK:
                    return False
                
        return True

    ### END: Helpers