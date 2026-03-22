from typing import Optional

from src.entities.board import Board
from src.entities.enums import GameStatus, PieceType


class DrawDetector:
    """Stateless detector for draw conditions."""

    def check_draw_conditions(self, board: Board) -> Optional[GameStatus]:
        """Check all draw conditions in order. Returns first match or None."""
        if self.is_insufficient_material(board):
            return GameStatus.DRAW_INSUFFICIENT_MATERIAL
        if self.is_threefold_repetition(board):
            return GameStatus.DRAW_THREEFOLD_REPETITION
        if self.is_fifty_move_rule(board):
            return GameStatus.DRAW_FIFTY_MOVE
        return None

    def is_insufficient_material(self, board: Board) -> bool:
        """Return True when neither side can force checkmate."""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece is not None:
                    pieces.append((piece, row, col))

        # K vs K
        if len(pieces) == 2:
            return True

        # K+minor vs K
        if len(pieces) == 3:
            for piece, _r, _c in pieces:
                if piece.piece_type in (PieceType.BISHOP, PieceType.KNIGHT):
                    return True

        # K+B vs K+B with same-color bishops
        if len(pieces) == 4:
            bishops = [
                (piece, r, c)
                for piece, r, c in pieces
                if piece.piece_type == PieceType.BISHOP
            ]
            if len(bishops) == 2:
                # Check if bishops are on the same color square
                _, r1, c1 = bishops[0]
                _, r2, c2 = bishops[1]
                if (r1 + c1) % 2 == (r2 + c2) % 2:
                    return True

        return False

    def is_threefold_repetition(self, board: Board) -> bool:
        """Return True when the current position has occurred three or more times."""
        if not board.position_history:
            return False
        current = board.position_history[-1]
        return board.position_history.count(current) >= 3

    def is_fifty_move_rule(self, board: Board) -> bool:
        """Return True when halfmove clock reaches 100 (50 full moves)."""
        return board.halfmove_clock >= 100
