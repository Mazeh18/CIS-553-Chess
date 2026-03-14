"""Tests for king movement rules."""

from src.entities.board import Board
from src.entities.position import Position
from src.entities.enums import Color, PieceType
from tests.conftest import place_piece


class TestKingBasicMoves:
    """Test basic king movement (one square in any direction)."""

    def test_king_moves_all_directions_from_center(self, empty_board, validator):
        """A king in the center can move to all 8 adjacent squares."""
        place_piece(empty_board, "e4", PieceType.KING, Color.WHITE)

        moves = validator.get_legal_moves(empty_board, Position.from_algebraic("e4"))
        expected = {
            Position.from_algebraic(sq)
            for sq in ["d5", "e5", "f5", "d4", "f4", "d3", "e3", "f3"]
        }
        assert set(moves) == expected

    def test_king_moves_from_corner(self, empty_board, validator):
        """A king in the corner has only 3 moves."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE)

        moves = validator.get_legal_moves(empty_board, Position.from_algebraic("a1"))
        expected = {Position.from_algebraic(sq) for sq in ["a2", "b2", "b1"]}
        assert set(moves) == expected

    def test_king_blocked_by_own_pieces(self, empty_board, validator):
        """King cannot move to squares occupied by own pieces."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "d1", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "f1", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "d2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "f2", PieceType.PAWN, Color.WHITE)

        moves = validator.get_legal_moves(empty_board, Position.from_algebraic("e1"))
        assert len(moves) == 0

    def test_king_can_capture_enemy(self, empty_board, validator):
        """King can capture an enemy piece."""
        place_piece(empty_board, "e4", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e5", PieceType.PAWN, Color.BLACK)

        moves = validator.get_legal_moves(empty_board, Position.from_algebraic("e4"))
        assert Position.from_algebraic("e5") in moves

    def test_king_cannot_move_into_check(self, empty_board, validator):
        """King cannot move to a square attacked by enemy."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.ROOK, Color.BLACK)

        moves = validator.get_legal_moves(empty_board, Position.from_algebraic("e1"))
        # e-file is controlled by the rook, so e2 is not legal
        assert Position.from_algebraic("e2") not in moves
        # d1, f1, d2, f2 should still be legal
        assert Position.from_algebraic("d1") in moves
        assert Position.from_algebraic("f1") in moves

    def test_king_cannot_move_adjacent_to_enemy_king(self, empty_board, validator):
        """Kings cannot be adjacent to each other."""
        place_piece(empty_board, "e4", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e6", PieceType.KING, Color.BLACK)

        moves = validator.get_legal_moves(empty_board, Position.from_algebraic("e4"))
        # e5 is attacked by black king, so white king can't go there
        assert Position.from_algebraic("e5") not in moves
