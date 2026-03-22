"""Tests for queen movement: combines rook and bishop, blocking, and captures."""

import pytest

from src.entities.position import Position
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece


class TestQueenCombinedMovement:
    """Queen combines rook (horizontal/vertical) and bishop (diagonal) movement."""

    def test_queen_horizontal_moves(self, empty_board, validator):
        """Queen on d4 can move horizontally."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["a4", "b4", "c4", "e4", "f4", "g4", "h4"]:
            assert Position.from_algebraic(sq) in moves

    def test_queen_vertical_moves(self, empty_board, validator):
        """Queen on d4 can move vertically."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in ["d1", "d2", "d3", "d5", "d6", "d7", "d8"]:
            assert Position.from_algebraic(sq) in moves

    def test_queen_diagonal_moves(self, empty_board, validator):
        """Queen on d4 can move diagonally."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        for sq in [
            "e5",
            "f6",
            "g7",
            "h8",
            "c5",
            "b6",
            "a7",
            "e3",
            "f2",
            "g1",
            "c3",
            "b2",
        ]:
            assert Position.from_algebraic(sq) in moves

    def test_queen_total_moves_open_board(self, empty_board, validator):
        """Queen on d4 on open board has 27 moves (14 rook + 13 bishop)."""
        place_piece(empty_board, "a2", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "h8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )

        moves = validator.get_legal_moves(empty_board, pos)
        assert len(moves) == 27


class TestQueenBlocking:
    """Queen blocked by own pieces."""

    def test_queen_blocked_by_own_piece_horizontal(self, empty_board, validator):
        """Queen on d4 blocked by own piece on f4 cannot reach f4 or beyond."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "f4", PieceType.ROOK, Color.WHITE, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e4") in moves
        assert Position.from_algebraic("f4") not in moves
        assert Position.from_algebraic("g4") not in moves

    def test_queen_blocked_by_own_piece_diagonal(self, empty_board, validator):
        """Queen on d4 blocked by own piece on f6 cannot reach f6 or beyond."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "f6", PieceType.BISHOP, Color.WHITE, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e5") in moves
        assert Position.from_algebraic("f6") not in moves
        assert Position.from_algebraic("g7") not in moves


class TestQueenCaptures:
    """Queen capturing enemy pieces."""

    def test_queen_captures_enemy_horizontal(self, empty_board, validator):
        """Queen on d4 can capture enemy on g4 but not pass through."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "g4", PieceType.ROOK, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e4") in moves
        assert Position.from_algebraic("f4") in moves
        assert Position.from_algebraic("g4") in moves  # capture
        assert Position.from_algebraic("h4") not in moves

    def test_queen_captures_enemy_diagonal(self, empty_board, validator):
        """Queen on d4 can capture enemy on f6 but not pass through."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.QUEEN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "f6", PieceType.KNIGHT, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e5") in moves
        assert Position.from_algebraic("f6") in moves  # capture
        assert Position.from_algebraic("g7") not in moves
