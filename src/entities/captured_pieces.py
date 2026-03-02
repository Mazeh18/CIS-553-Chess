from typing import Optional

from src.entities.enums import Color
from src.entities.piece import Piece


class CapturedPieces:
    """Tracks captured pieces for both players and calculates point advantage."""

    def __init__(self) -> None:
        self.white_captured: list[Piece] = []  # pieces captured BY White (Black's lost pieces)
        self.black_captured: list[Piece] = []  # pieces captured BY Black (White's lost pieces)

    def add_captured(self, piece: Piece) -> None:
        """Add a captured piece to the appropriate list based on the piece's color."""
        if piece.color == Color.WHITE:
            self.black_captured.append(piece)
        else:
            self.white_captured.append(piece)

    def remove_last_captured(self, color: Color) -> Optional[Piece]:
        """Remove and return the last piece captured by the given color. For undo support."""
        target = self.white_captured if color == Color.WHITE else self.black_captured
        if target:
            return target.pop()
        return None

    def get_points(self, color: Color) -> int:
        """Get total points of pieces captured by the given color."""
        target = self.white_captured if color == Color.WHITE else self.black_captured
        return sum(p.value() for p in target)

    def get_point_advantage(self) -> int:
        """Return point advantage. Positive = White leads, negative = Black leads."""
        return self.get_points(Color.WHITE) - self.get_points(Color.BLACK)
