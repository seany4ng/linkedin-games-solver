from typing import Any
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations
import time

class SolutionEnum(Enum):
    BLANK = -1
    X = 0
    QUEEN = 1

class RuleEnum(Enum):
    SOLVE_LAST = 0
    REDUCE_SETS = 1
    FIND_INVALID_TILES = 2
    # TODO: add more rules

INT_TO_VALUE_TYPE = {
    -1: SolutionEnum.BLANK,
    0: SolutionEnum.X,
    1: SolutionEnum.QUEEN,
}

VALUE_TYPE_TO_INT = {v: k for k, v in INT_TO_VALUE_TYPE.items()}

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class Board:
    def __init__(self, board_size: int, board: list[list[int]]):
        if len(board) != board_size or len(board[0]) != board_size:
            raise ValueError("Invalid board inputted")
        
        self.board = board
        self.board_size = board_size
        self.solution = [[SolutionEnum.BLANK for _ in range(board_size)] for _ in range(board_size)]
        self.color_to_rows, self.color_to_cols = [set() for _ in range(self.board_size + 1)], [set() for _ in range(self.board_size + 1)]


    def iterate_once(self):
        print(f"Starting iteration with solution:\n{[[VALUE_TYPE_TO_INT[x] for x in row] for row in self.solution]}")
        print(f"Color-to-Rows:\n{self.color_to_rows}")
        print(f"Color-to-Cols:\n{self.color_to_cols}")

        for rule in RuleEnum:
            match rule:
                case RuleEnum.SOLVE_LAST:
                    self.solve_last()
                case RuleEnum.REDUCE_SETS:
                    self.reduce_sets(self.color_to_rows)
                    self.reduce_sets(self.color_to_cols)
                case RuleEnum.FIND_INVALID_TILES:
                    self.find_invalid_tiles()
            self.update_sets()

    def solve_board(self):
        self.update_sets()
        while not self.is_solved():
            self.iterate_once()
            

    ### BEGIN: Rules
    
    def solve_last(self):
        """Place queen if last in row/col/color"""

        # If one blank left in row
        for i in range(self.board_size):
            if self.solution[i].count(SolutionEnum.BLANK) == 1:
                col_index = self.solution[i].index(SolutionEnum.BLANK)
                self.place_queen(i, col_index)
                print("Queen placed in row", i, "col", col_index)
        
        # If one blank left in col
        for j, col in enumerate(zip(*self.solution)):
            blanks = [i for i, value in enumerate(col) if value == SolutionEnum.BLANK]
            if len(blanks) == 1:
                row_index = blanks[0]
                self.place_queen(row_index, j)
                print("Queen placed in row", row_index, "col", j)
        
        # If one blank left in color
        for color in range(self.board_size):
            if len(self.color_to_rows[color]) == len(self.color_to_cols[color]) == 1:
                [row_index] = self.color_to_rows[color]
                [col_index] = self.color_to_cols[color]
                self.place_queen(row_index, col_index)
                print("Queen placed in row", row_index, "col", col_index)

    def power_set(self, iterable):
        s = list(iterable)
        for r in range(1, len(s) + 1):
            for combo in combinations(s, r):
                yield combo

    def reduce_sets(self, sets: list[set[int]]):
        
        for subset in self.power_set(set([i for i in range(1, self.board_size+1)])):
            subset_frozen = frozenset(subset)
            subsets = set()
            for color in sets:
                if color.issubset(subset):
                    subsets.add(frozenset(color))
            if len(subsets) == len(subset):
                for i, rowcols in enumerate(sets):
                    if frozenset(rowcols) not in subsets:
                        sets[i] = rowcols - subset
        
    # def reduce_sets(self, sets: list[set[int]]):
    #     """Reduces the given color to rows/cols mapping if n colors are confined to n rows/columns."""
    
    #     # Identify groups of n colors in n rows/columns
    #     index_to_colors = defaultdict(set) 
    #     for color, indices in enumerate(sets):
    #         if indices:
    #             index_to_colors[frozenset(indices)].add(color)

    #     # Update sets with valid combinations
    #     for indices, colors in index_to_colors.items():
    #         if len(indices) == len(colors):  
    #             for color in colors:
    #                 sets[color].intersection_update(indices)

    #     # Cross off all tiles that do not follow these rules
    #     for i in range(self.board_size):
    #         for j in range(self.board_size):
    #             if self.solution[i][j] == SolutionEnum.BLANK and i not in sets[self.board[i][j]]:
    #                 self.solution[i][j] == SolutionEnum.X
        
    #     # print(sets)

    def find_invalid_tiles(self):
        """Identify and mark tiles where placing a queen would result in invalidating all position for a specific color elsewhere"""
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.solution[x][y] == SolutionEnum.BLANK:
                    invalid_tiles = self.simulate_placement(x, y)
                    # print("Invalid tiles for", x, y, ":", invalid_tiles)
                    if self.check_conflicts(invalid_tiles):
                        self.solution[x][y] = SolutionEnum.X
                        # print("Crossed out", x, y)

    ### END: Rules

    ### BEGIN: Helpers

    def place_queen(self, x, y):
        """Place queen on board (and cross out row, col, surrounding, and same colors)"""

        # Cross out same row and col
        for i in range(self.board_size):
            self.solution[x][i] = SolutionEnum.X
            self.solution[i][y] = SolutionEnum.X
        
        # Cross out surrounding tiles
        for dx, dy in directions:
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

    def simulate_placement(self, x: int, y: int) -> set[tuple[int]]:
        """Simulate placing a queen at (x, y) and calculate resulting invalid tiles"""

        invalid_tiles = set()

        # Add tiles in same row/col
        for i in range(self.board_size):
            invalid_tiles.add((x, i))
            invalid_tiles.add((i, y))
        
        # Remove tiles in same row/col
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                invalid_tiles.add((nx, ny))
        
        invalid_tiles.remove((x, y))
        return invalid_tiles

    def check_conflicts(self, invalid_tiles: set[tuple[int]]) -> bool:
        """Check conflicts for each color"""
        for color in range(1, self.board_size + 1):  
            # Get remaining tiles for specific color
            remaining_tiles = set(
                (x, y)
                for x in range(self.board_size) 
                for y in range(self.board_size) 
                if self.board[x][y] == color and self.solution[x][y] == SolutionEnum.BLANK
            )
            # Check if any of these tiles are invalid
            if remaining_tiles.issubset(invalid_tiles):
                return True  
        return False 

    def is_solved(self) -> bool:
        """Returns whether the board is fully solved or not"""
        for row in self.solution:
            for col in row:
                if col == SolutionEnum.BLANK:
                    return False
        return True

    ### END: Helpers