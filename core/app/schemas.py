from dataclasses import dataclass
from typing import List


@dataclass
class TangoSolveRequest:
    board: List[List[str]]
    vertical_lines: List[List[str]]
    horizontal_lines: List[List[str]]

@dataclass
class QueensSolveRequest:
    board_size: int
    board: List[List[int]]


@dataclass
class TangoGenerationResponse:
    board: list[list[str]]
    row_lines: list[list[str]]
    col_lines: list[list[str]]
    solution: list[list[str]]


@dataclass
class QueensGenerationResponse:
    board_size: int
    board: list[list[int]]
    solution: list[int]
