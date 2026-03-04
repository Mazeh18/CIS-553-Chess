from src.entities.enums import PieceType, Color

PIECE_VALUES = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 9,
    PieceType.KING: 0,
}

PIECE_SYMBOLS = {
    (PieceType.KING, Color.WHITE): "\u2654",
    (PieceType.QUEEN, Color.WHITE): "\u2655",
    (PieceType.ROOK, Color.WHITE): "\u2656",
    (PieceType.BISHOP, Color.WHITE): "\u2657",
    (PieceType.KNIGHT, Color.WHITE): "\u2658",
    (PieceType.PAWN, Color.WHITE): "\u2659",
    (PieceType.KING, Color.BLACK): "\u265a",
    (PieceType.QUEEN, Color.BLACK): "\u265b",
    (PieceType.ROOK, Color.BLACK): "\u265c",
    (PieceType.BISHOP, Color.BLACK): "\u265d",
    (PieceType.KNIGHT, Color.BLACK): "\u265e",
    (PieceType.PAWN, Color.BLACK): "\u265f",
}


class Piece:
    """Represents a single chess piece."""

    def __init__(
        self, piece_type: PieceType, color: Color, has_moved: bool = False
    ) -> None:
        self.piece_type = piece_type
        self.color = color
        self.has_moved = has_moved

    def value(self) -> int:
        """Return standard point value (Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9, King=0)."""
        return PIECE_VALUES[self.piece_type]

    def icon(self) -> str:
        """Return the visual representation of this piece."""
        return PIECE_SYMBOLS[(self.piece_type, self.color)]

    def __repr__(self) -> str:
        return f"Piece({self.piece_type.name}, {self.color.name})"
