from enum import Enum
from itertools import combinations
from typing import Any

import copy

from core.app.exceptions import QueensBoardInsufficientException, QueensBoardSolvedIncorrectlyException


class SolutionEnum(Enum):
    BLANK = -1
    X = 0
    QUEEN = 1


class RuleEnum(Enum):
    SOLVE_LAST = 0
    REDUCE_SETS = 1
    FIND_INVALID_TILES = 2


INT_TO_VALUE_TYPE = {
    -1: SolutionEnum.BLANK,
    0: SolutionEnum.X,
    1: SolutionEnum.QUEEN,
}
VALUE_TYPE_TO_INT = {v: k for k, v in INT_TO_VALUE_TYPE.items()}
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class QueensBoard:
    def __init__(self, board_size: int, board: list[list[int]]):
        if len(board) != board_size or len(board[0]) != board_size:
            raise ValueError("Invalid board inputted")
        
        self.board = board
        self.board_size = board_size
        self.solution = [[SolutionEnum.BLANK for _ in range(board_size)] for _ in range(board_size)]
        self.color_to_rows, self.color_to_cols = [set() for _ in range(self.board_size + 1)], [set() for _ in range(self.board_size + 1)]


    def iterate_once(self):
        """Performs one iteration of executing rules"""
        for rule in RuleEnum:
            match rule:
                case RuleEnum.SOLVE_LAST:
                    self.solve_last()
                case RuleEnum.REDUCE_SETS:
                    self.reduce_sets(self.color_to_rows, is_row=True)
                    self.reduce_sets(self.color_to_cols, is_row=False)
                case RuleEnum.FIND_INVALID_TILES:
                    self.find_invalid_tiles()
            self.update_sets()


    def solve_board(self):
        """Solves the Queens board"""
        self.update_sets()
        while not self.is_solved():
            prev_board: list[list[Any]] = copy.deepcopy(self.solution)
            self.iterate_once()
            if prev_board == self.solution:
                raise QueensBoardInsufficientException()
            
        if not self.solved_board_is_correct():
            raise QueensBoardSolvedIncorrectlyException()
            

    ### BEGIN: Rules
    
    def solve_last(self):
        """
        RULE 1: If there is only a single blank left in a row, column, or color,
        we place a queen in that remaining blank.
        """

        # If one blank left in row
        for i in range(self.board_size):
            if self.solution[i].count(SolutionEnum.BLANK) == 1:
                col_index = self.solution[i].index(SolutionEnum.BLANK)
                self.place_queen(i, col_index)
        
        # If one blank left in col
        for j, col in enumerate(zip(*self.solution)):
            blanks = [i for i, value in enumerate(col) if value == SolutionEnum.BLANK]
            if len(blanks) == 1:
                row_index = blanks[0]
                self.place_queen(row_index, j)
        
        # If one blank left in color
        for color in range(self.board_size):
            if len(self.color_to_rows[color]) == len(self.color_to_cols[color]) == 1:
                [row_index] = self.color_to_rows[color]
                [col_index] = self.color_to_cols[color]
                self.place_queen(row_index, col_index)


    def reduce_sets(self, sets: list[set[int]], is_row: bool):
        for subset in self.power_set_of_row_col(self.board_size):
            # Represents the indices that should not be eliminated
            subset_indices = set()
            for i, color in enumerate(sets):
                if color.issubset(subset) and len(color) > 0:
                    subset_indices.add(i)

            if len(subset_indices) == len(subset):
                for i, rowcols in enumerate(sets):
                    if i not in subset_indices:
                        sets[i] = rowcols - subset
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.solution[i][j] == SolutionEnum.BLANK:
                    if is_row and i not in sets[self.board[i][j]]:
                        self.solution[i][j] = SolutionEnum.X
                    elif not is_row and j not in sets[self.board[i][j]]:
                        self.solution[i][j] = SolutionEnum.X


    def find_invalid_tiles(self):
        """Identify and mark tiles where placing a queen would result in invalidating all position for a specific color elsewhere"""

        remaining_tiles = [self.get_remaining_tiles(color) for color in range(1, self.board_size + 1)]

        # Find invalid tiles for colors. i.e. if placing a Queen in a tile eliminates an entire color,
        # we can put an X in that tile.
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.solution[x][y] == SolutionEnum.BLANK:
                    invalid_tiles = self.simulate_placement(x, y)
                    if self.check_conflicts(invalid_tiles, remaining_tiles):
                        self.solution[x][y] = SolutionEnum.X

    ### END: Rules

    ### BEGIN: Helpers

    def power_set_of_row_col(self, board_size: int):
        """Returns the power set of all possible row/column combos"""
        for r in range(board_size):
            for combo in combinations(range(board_size), r):
                yield {val for val in combo}


    def place_queen(self, x, y):
        """Place queen on board (and cross out row, col, surrounding, and same colors)"""

        # Cross out same row and col
        for i in range(self.board_size):
            self.solution[x][i] = SolutionEnum.X
            self.solution[i][y] = SolutionEnum.X
        
        # Cross out surrounding tiles
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                self.solution[nx][ny] = SolutionEnum.X

        # Cross out tiles of same color
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == self.board[x][y]:
                    self.solution[i][j] = SolutionEnum.X
        
        self.solution[x][y] = SolutionEnum.QUEEN

    def update_sets(self):
        """Update sets when tiles crossed off"""
        # Clear current mappings
        self.color_to_rows = [set() for _ in range(self.board_size + 1)]
        self.color_to_cols = [set() for _ in range(self.board_size + 1)]

        # Add row and col to color set
        for i in range(self.board_size):  
            for j in range(self.board_size):  
                if self.solution[i][j] == SolutionEnum.BLANK:
                    self.color_to_rows[self.board[i][j]].add(i)
                    self.color_to_cols[self.board[i][j]].add(j)

    def simulate_placement(self, x: int, y: int) -> set[tuple[int, int]]:
        """Simulate placing a queen at (x, y) and calculate resulting invalid tiles"""

        invalid_tiles = set()

        # Add tiles in same row/col
        for i in range(self.board_size):
            invalid_tiles.add((x, i))
            invalid_tiles.add((i, y))
        
        # Remove tiles in same row/col
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                invalid_tiles.add((nx, ny))
        
        invalid_tiles.remove((x, y))
        return invalid_tiles


    def get_remaining_tiles(self, color: int) -> set[tuple[int, int]]:
        """Get remaining tiles for a specific color"""
        return set(
            (x, y)
            for x in range(self.board_size) 
            for y in range(self.board_size) 
            if self.board[x][y] == color and self.solution[x][y] == SolutionEnum.BLANK
        )


    def check_conflicts(self, invalid_tiles: set[tuple[int, int]], remaining_tiles: list[set[tuple[int, int]]]) -> bool:
        """
        Determines if placing a queen will eliminate all blanks for either
        a color, a row, or a column. return True if it would, and False otherwise.
        """
        for color in remaining_tiles:
            if color != set() and color.issubset(invalid_tiles):
                return True
            
        # Check row-wise first
        for r in range(self.board_size):
            if SolutionEnum.QUEEN not in self.solution[r]:
                # 
                should_eliminate = True
                for c in range(self.board_size):
                    # If statement is hit if this (r, c) blank does not get eliminated by invalid tile.
                    if self.solution[r][c] == SolutionEnum.BLANK and (r, c) not in invalid_tiles:
                        should_eliminate = False

                if should_eliminate:
                    return True
                
        # Now check column-wise
        for c, col in enumerate(zip(*self.solution)):
            if SolutionEnum.QUEEN not in col:
                should_eliminate = True
                for r in range(self.board_size):
                    # If statement is hit if this (r, c) blank does not get eliminated by invalid tile.
                    if self.solution[r][c] == SolutionEnum.BLANK and (r, c) not in invalid_tiles:
                        should_eliminate = False

                if should_eliminate:
                    return True
                    
        return False 


    def is_solved(self) -> bool:
        """Returns whether the board is fully solved or not"""
        for row in self.solution:
            for col in row:
                if col == SolutionEnum.BLANK:
                    return False
        return True

    def solved_board_is_correct(self) -> bool:
        """Returns whether `self.solution` follows the rules"""
        row_occurences, col_occurences = set(), set()
        for r in range(len(self.solution)):
            for c in range(len(self.solution[r])):
                if self.solution[r][c] == SolutionEnum.QUEEN:
                    row_occurences.add(r)
                    col_occurences.add(c)

                    conflicts: set[tuple[int, int]] = self.simulate_placement(r, c)
                    for x, y in conflicts:
                        if self.solution[x][y] == SolutionEnum.QUEEN:
                            return False

        # If there are columns or rows with missing queens, consider this board
        # underspecified.
        if not row_occurences == col_occurences == set(range(len(self.board))):
            raise QueensBoardInsufficientException()
        
        return True

    ### END: Helpers
