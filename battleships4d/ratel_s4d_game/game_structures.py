from enum import Enum


class CellState(Enum):
    EMPTY = 0
    MISSED = 1
    FUNCTIONAL = 2
    DAMAGED = 3
    DEAD = 4
    MARKED = 5


class GamePhase(Enum):
    INITIAL = 0
    BATTLE = 1
    CONCLUSION = 2


class EndState(Enum):
    WIN = 0
    LOSS = 1
    DRAW = 2


class Board4D:
    def __init__(self):
        self.space = [[[[CellState.EMPTY for _ in range(5)] for _ in range(5)] for _ in range(5)] for _ in range(5)]
