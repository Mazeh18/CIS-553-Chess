"""Tests for knight movement: L-shaped jumps, jumping over pieces, captures."""

import pytest

from src.entities.position import Position
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece


class TestKnightLShapedMoves:
    """Knight L-shaped movement from center position."""

    def test_knight_all_eight_moves_from_center(self, empty_board, validator):
        """Knight on d4 has all 8 L-shaped destination squares."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        expected = {
            Position.from_algebraic(sq)
            for sq in ["c6", "e6", "b5", "f5", "b3", "f3", "c2", "e2"]
        }
        assert expected == moves

    def test_knight_count_from_center(self, empty_board, validator):
        """Knight on d4 with no obstructions has exactly 8 moves."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )

        moves = validator.get_legal_moves(empty_board, pos)
        assert len(moves) == 8


class TestKnightJumping:
    """Knight can jump over other pieces."""

    def test_knight_jumps_over_own_pieces(self, empty_board, validator):
        """Knight on b1 surrounded by own pawns can still reach its squares."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(empty_board, "b1", PieceType.KNIGHT, Color.WHITE)
        # Surround with own pawns
        place_piece(empty_board, "a2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "b2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "c2", PieceType.PAWN, Color.WHITE)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("a3") in moves
        assert Position.from_algebraic("c3") in moves
        # d2 is also a valid L-shaped move from b1
        assert Position.from_algebraic("d2") in moves

    def test_knight_jumps_over_enemy_pieces(self, empty_board, validator):
        """Knight on d4 surrounded by enemy pieces can still reach all 8 squares."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )
        # Place enemy pieces in all adjacent squares
        for sq in ["c4", "e4", "d3", "d5", "c3", "e3", "c5", "e5"]:
            place_piece(empty_board, sq, PieceType.PAWN, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert len(moves) == 8


class TestKnightOwnPieceBlocking:
    """Knight cannot land on own pieces."""

    def test_knight_cannot_land_on_own_piece(self, empty_board, validator):
        """Knight on d4 cannot move to c6 if own piece is there."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "c6", PieceType.PAWN, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e6", PieceType.BISHOP, Color.WHITE, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("c6") not in moves
        assert Position.from_algebraic("e6") not in moves
        # Other squares should still be available
        assert Position.from_algebraic("b5") in moves
        assert Position.from_algebraic("f5") in moves


class TestKnightCaptures:
    """Knight capturing enemy pieces."""

    def test_knight_captures_enemy_piece(self, empty_board, validator):
        """Knight on d4 can capture enemy piece on c6."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "c6", PieceType.ROOK, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("c6") in moves

    def test_knight_captures_multiple_enemies(self, empty_board, validator):
        """Knight on d4 can capture multiple enemy pieces at different L-positions."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "c6", PieceType.PAWN, Color.BLACK)
        place_piece(empty_board, "f5", PieceType.BISHOP, Color.BLACK, has_moved=True)
        place_piece(empty_board, "e2", PieceType.ROOK, Color.BLACK, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("c6") in moves
        assert Position.from_algebraic("f5") in moves
        assert Position.from_algebraic("e2") in moves


class TestKnightCorner:
    """Knight has limited moves from corner and edge positions."""

    def test_knight_from_corner_a1(self, empty_board, validator):
        """Knight on a1 has only 2 possible moves: b3 and c2."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "a1", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        expected = {Position.from_algebraic("b3"), Position.from_algebraic("c2")}
        assert moves == expected

    def test_knight_from_corner_h8(self, empty_board, validator):
        """Knight on h8 has only 2 possible moves: g6 and f7."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "h8", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        expected = {Position.from_algebraic("g6"), Position.from_algebraic("f7")}
        assert moves == expected

    def test_knight_from_edge_a4(self, empty_board, validator):
        """Knight on a4 has 4 possible moves."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "a4", PieceType.KNIGHT, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        expected = {
            Position.from_algebraic("b6"),
            Position.from_algebraic("c5"),
            Position.from_algebraic("c3"),
            Position.from_algebraic("b2"),
        }
        assert moves == expected
