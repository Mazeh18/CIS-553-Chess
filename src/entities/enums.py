from enum import Enum, auto


class ScreenType(Enum):
    START_MENU = auto()
    CREDITS = auto()
    TIME_SELECT = auto()
    GAME = auto()


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class PieceType(Enum):
    PAWN = auto()
    ROOK = auto()
    KNIGHT = auto()
    BISHOP = auto()
    QUEEN = auto()
    KING = auto()
