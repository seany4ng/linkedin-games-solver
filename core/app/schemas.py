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
    diffs: list[list[str]]
    eqs: list[list[str]]
    solution: list[list[str]]
