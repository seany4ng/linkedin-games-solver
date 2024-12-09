from dataclasses import dataclass
from typing import List


@dataclass
class TangoSolveRequest:
    board: List[List[str]]
    vertical_lines: List[List[str]]
    horizontal_lines: List[List[str]]
