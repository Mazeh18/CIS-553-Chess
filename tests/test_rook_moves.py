"""Tests for rook movement: horizontal/vertical sliding, blocking, and captures."""

import pytest

from src.entities.position import Position
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece


class TestRookSliding:
    """Rook horizontal and vertical movement on an open board."""

    def test_rook_horizontal_right(self, empty_board, validator):
        """Rook on d4 can slide right to e4, f4, g4, h4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.ROOK, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["e4", "f4", "g4", "h4"]:
            assert Position.from_algebraic(sq) in moves

    def test_rook_horizontal_left(self, empty_board, validator):
        """Rook on d4 can slide left to c4, b4, a4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.ROOK, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["c4", "b4", "a4"]:
            assert Position.from_algebraic(sq) in moves

    def test_rook_vertical_up(self, empty_board, validator):
        """Rook on d4 can slide up to d5, d6, d7, d8."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.ROOK, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["d5", "d6", "d7", "d8"]:
            assert Position.from_algebraic(sq) in moves

    def test_rook_vertical_down(self, empty_board, validator):
        """Rook on d4 can slide down to d3, d2, d1."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.ROOK, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["d3", "d2", "d1"]:
            assert Position.from_algebraic(sq) in moves

    def test_rook_total_moves_open_board(self, empty_board, validator):
        """Rook on d4 on open board has 14 moves (7 horizontal + 7 vertical)."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.ROOK, Color.WHITE, has_moved=True
        )

        moves = validator.get_legal_moves(empty_board, pos)
        assert len(moves) == 14


class TestRookBlocking:
    """Rook blocked by own pieces."""

    def test_rook_blocked_by_own_piece(self, empty_board, validator):
        """Rook on a1 blocked by own pawn on a3 cannot reach a3 or beyond."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "a1", PieceType.ROOK, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "a3", PieceType.PAWN, Color.WHITE, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("a2") in moves
        assert Position.from_algebraic("a3") not in moves
        assert Position.from_algebraic("a4") not in moves

    def test_rook_cannot_jump_over_pieces(self, empty_board, validator):
        """Rook on a1 with blocker on a3 cannot reach a5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "a1", PieceType.ROOK, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "a3", PieceType.PAWN, Color.BLACK)

        moves = set(validator.get_legal_moves(empty_board, pos))
        # Can capture a3 but cannot go beyond
        assert Position.from_algebraic("a3") in moves
        assert Position.from_algebraic("a4") not in moves
        assert Position.from_algebraic("a5") not in moves


class TestRookCaptures:
    """Rook capturing enemy pieces."""

    def test_rook_captures_enemy_and_stops(self, empty_board, validator):
        """Rook on d1 can capture enemy on d5 but cannot go to d6."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d1", PieceType.ROOK, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "d5", PieceType.BISHOP, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d2") in moves
        assert Position.from_algebraic("d3") in moves
        assert Position.from_algebraic("d4") in moves
        assert Position.from_algebraic("d5") in moves  # capture
        assert Position.from_algebraic("d6") not in moves

    def test_rook_no_diagonal_moves(self, empty_board, validator):
        """Rook should have no diagonal moves."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.ROOK, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["e5", "c3", "e3", "c5"]:
            assert Position.from_algebraic(sq) not in moves
