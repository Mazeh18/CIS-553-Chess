from typing import Optional, Callable

from src.entities.position import Position
from src.entities.board import Board
from src.entities.drag_state import DragState
from src.entities.move_attempt import MoveAttempt
from src.entities.enums import Color


class InputController:
    """Translates Pygame mouse events into game-level actions. Manages DragState."""

    def __init__(
        self,
        drag_state: DragState,
        board_x: int,
        board_y: int,
        square_size: int,
        get_legal_moves_fn: Callable,
        get_current_turn_fn: Callable,
    ) -> None:
        self._drag_state = drag_state
        self._board_x = board_x
        self._board_y = board_y
        self._square_size = square_size
        self._get_legal_moves = get_legal_moves_fn
        self._get_current_turn = get_current_turn_fn

    def handle_mouse_down(
        self, pixel_pos: tuple, board: Board
    ) -> None:
        """On mouse down: if clicking own piece, start drag with legal moves."""
        pos = self.pixel_to_board_position(pixel_pos)
        if pos is None:
            return

        piece = board.get_piece(pos)
        if piece is None:
            return

        current_turn = self._get_current_turn()
        if piece.color != current_turn:
            return

        legal_moves = self._get_legal_moves(pos)
        self._drag_state.start_drag(piece, pos, legal_moves)
        self._drag_state.update_mouse(pixel_pos)

    def handle_mouse_motion(self, pixel_pos: tuple) -> None:
        """On mouse motion: update drag position."""
        if self._drag_state.is_dragging:
            self._drag_state.update_mouse(pixel_pos)

    def handle_mouse_up(
        self, pixel_pos: tuple
    ) -> Optional[MoveAttempt]:
        """On mouse up: if valid destination, return MoveAttempt; else cancel drag."""
        if not self._drag_state.is_dragging:
            return None

        origin = self._drag_state.origin
        legal_moves = list(self._drag_state.legal_moves)
        target = self.pixel_to_board_position(pixel_pos)

        # Reset drag state before returning
        self._drag_state.reset()

        if target is None or origin is None:
            return None

        # Only return a MoveAttempt if the target is a legal destination
        if target in legal_moves:
            return MoveAttempt(origin, target)

        return None

    def pixel_to_board_position(
        self, pixel_pos: tuple
    ) -> Optional[Position]:
        """Convert screen pixel coordinates to a board Position."""
        px, py = pixel_pos
        col = (px - self._board_x) // self._square_size
        row = (py - self._board_y) // self._square_size

        pos = Position(row, col)
        if pos.is_valid():
            return pos
        return None
