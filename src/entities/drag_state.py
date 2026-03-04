from typing import Optional

from src.entities.position import Position
from src.entities.piece import Piece


class DragState:
    """Tracks the current drag-and-drop interaction state."""

    def __init__(self) -> None:
        self.is_dragging: bool = False
        self.piece: Optional[Piece] = None
        self.origin: Optional[Position] = None
        self.mouse_pos: Optional[tuple] = None
        self.legal_moves: list[Position] = []

    def start_drag(self, piece: Piece, origin: Position, moves: list[Position]) -> None:
        """Begin a drag interaction."""
        self.is_dragging = True
        self.piece = piece
        self.origin = origin
        self.legal_moves = moves

    def update_mouse(self, pos: tuple) -> None:
        """Update the current mouse position during drag."""
        self.mouse_pos = pos

    def cancel_drag(self) -> None:
        """Cancel the current drag and reset state."""
        self.reset()

    def reset(self) -> None:
        """Clear all drag state."""
        self.is_dragging = False
        self.piece = None
        self.origin = None
        self.mouse_pos = None
        self.legal_moves = []
