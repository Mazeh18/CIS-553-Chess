from typing import Optional

from src.entities.enums import PieceType
from src.entities.position import Position
from src.entities.piece import Piece


class Move:
    """Represents a single move with all metadata for undo support."""

    def __init__(
        self,
        piece: Piece,
        start_pos: Position,
        end_pos: Position,
        captured_piece: Optional[Piece] = None,
        is_castling: bool = False,
        is_en_passant: bool = False,
        promotion_piece: Optional[PieceType] = None,
        notation: str = "",
        time_after_move: Optional[float] = None,
    ) -> None:
        self.piece = piece
        self.had_moved = piece.has_moved
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.captured_piece = captured_piece
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.promotion_piece = promotion_piece
        self.notation = notation
        self.time_after_move = time_after_move

    def __repr__(self) -> str:
        return f"Move({self.piece}, {self.start_pos} -> {self.end_pos})"
