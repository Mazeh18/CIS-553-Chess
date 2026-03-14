"""Tests for bishop movement: diagonal sliding, blocking, and captures."""

import pytest

from src.entities.position import Position
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece


class TestBishopDiagonals:
    """Bishop movement in all four diagonal directions."""

    def test_bishop_northeast(self, empty_board, validator):
        """Bishop on d4 can slide northeast to e5, f6, g7, h8."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.BISHOP, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["e5", "f6", "g7", "h8"]:
            assert Position.from_algebraic(sq) in moves

    def test_bishop_northwest(self, empty_board, validator):
        """Bishop on d4 can slide northwest to c5, b6, a7."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.BISHOP, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["c5", "b6", "a7"]:
            assert Position.from_algebraic(sq) in moves

    def test_bishop_southeast(self, empty_board, validator):
        """Bishop on d4 can slide southeast to e3, f2, g1."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.BISHOP, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["e3", "f2", "g1"]:
            assert Position.from_algebraic(sq) in moves

    def test_bishop_southwest(self, empty_board, validator):
        """Bishop on d4 can slide southwest to c3, b2."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.BISHOP, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["c3", "b2"]:
            assert Position.from_algebraic(sq) in moves

    def test_bishop_total_moves_open_board(self, empty_board, validator):
        """Bishop on d4 on open board has 13 diagonal squares."""
        place_piece(empty_board, "a2", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.BISHOP, Color.WHITE, has_moved=True
        )

        moves = validator.get_legal_moves(empty_board, pos)
        assert len(moves) == 13


class TestBishopBlocking:
    """Bishop blocked by own pieces and cannot jump."""

    def test_bishop_blocked_by_own_piece(self, empty_board, validator):
        """Bishop on c1 blocked by own pawn on e3 cannot reach e3 or f4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "c1", PieceType.BISHOP, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "e3", PieceType.PAWN, Color.WHITE, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d2") in moves
        assert Position.from_algebraic("e3") not in moves
        assert Position.from_algebraic("f4") not in moves

    def test_bishop_cannot_jump_over_pieces(self, empty_board, validator):
        """Bishop on a1 with blocker on c3 cannot reach d4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "a1", PieceType.BISHOP, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "c3", PieceType.KNIGHT, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("b2") in moves
        assert Position.from_algebraic("c3") in moves  # capture
        assert Position.from_algebraic("d4") not in moves


class TestBishopCaptures:
    """Bishop capturing enemy pieces."""

    def test_bishop_captures_enemy_and_stops(self, empty_board, validator):
        """Bishop on a1 can capture enemy on d4 but cannot go to e5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "a1", PieceType.BISHOP, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "d4", PieceType.PAWN, Color.BLACK)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("b2") in moves
        assert Position.from_algebraic("c3") in moves
        assert Position.from_algebraic("d4") in moves  # capture
        assert Position.from_algebraic("e5") not in moves

    def test_bishop_no_horizontal_or_vertical_moves(self, empty_board, validator):
        """Bishop should have no horizontal or vertical moves."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.BISHOP, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["d5", "d3", "e4", "c4"]:
            assert Position.from_algebraic(sq) not in moves
