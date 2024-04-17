from enum import Enum

class MoveType(Enum):
    FOLD = "FOLD"
    BET = "BET"
    CHECK = "CHECK"
    CALL = "CALL"
    RAISE = "RAISE"

class Move:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value