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


class GameStatus(Enum):
    ACTIVE = auto()
    CHECK = auto()
    CHECKMATE = auto()
    STALEMATE = auto()
    DRAW_INSUFFICIENT_MATERIAL = auto()
    DRAW_THREEFOLD_REPETITION = auto()
    DRAW_FIFTY_MOVE = auto()
    RESIGNED = auto()
    TIMEOUT = auto()

    def is_game_over(self) -> bool:
        return self in (
            GameStatus.CHECKMATE,
            GameStatus.STALEMATE,
            GameStatus.DRAW_INSUFFICIENT_MATERIAL,
            GameStatus.DRAW_THREEFOLD_REPETITION,
            GameStatus.DRAW_FIFTY_MOVE,
            GameStatus.RESIGNED,
            GameStatus.TIMEOUT,
        )

    def is_draw(self) -> bool:
        return self in (
            GameStatus.STALEMATE,
            GameStatus.DRAW_INSUFFICIENT_MATERIAL,
            GameStatus.DRAW_THREEFOLD_REPETITION,
            GameStatus.DRAW_FIFTY_MOVE,
        )
