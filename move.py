from enum import Enum

class MoveType(Enum):
    FOLD = "Fold"
    BET = "Bet"
    CHECK = "Check"
    CALL = "Call"
    RAISE = "Raise"

class Move:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value