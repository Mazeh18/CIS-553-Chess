"""Tests for pawn movement, captures, en passant, and promotion."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.move import Move
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece


class TestPawnForwardMoves:
    """Pawn single and double forward moves."""

    def test_white_pawn_forward_one(self, empty_board, validator):
        """White pawn on e4 can move to e5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e4", PieceType.PAWN, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e5") in moves

    def test_black_pawn_forward_one(self, empty_board, validator):
        """Black pawn on d5 can move to d4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d5", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        empty_board.current_turn = Color.BLACK

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d4") in moves

    def test_white_pawn_double_from_start(self, empty_board, validator):
        """White pawn on e2 (starting rank) can move to e3 and e4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e3") in moves
        assert Position.from_algebraic("e4") in moves

    def test_black_pawn_double_from_start(self, empty_board, validator):
        """Black pawn on d7 (starting rank) can move to d6 and d5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(empty_board, "d7", PieceType.PAWN, Color.BLACK)
        empty_board.current_turn = Color.BLACK

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d6") in moves
        assert Position.from_algebraic("d5") in moves


class TestPawnBlocked:
    """Pawn cannot move forward when blocked."""

    def test_white_pawn_blocked_by_piece(self, empty_board, validator):
        """White pawn on e4 cannot move forward if e5 is occupied."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e4", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "e5", PieceType.PAWN, Color.BLACK)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e5") not in moves

    def test_white_pawn_double_blocked_on_first_square(self, empty_board, validator):
        """White pawn on e2 cannot double-move if e3 is blocked."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "e3", PieceType.KNIGHT, Color.BLACK)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e3") not in moves
        assert Position.from_algebraic("e4") not in moves

    def test_white_pawn_double_blocked_on_second_square(self, empty_board, validator):
        """White pawn on e2 cannot double-move if e4 is blocked, but can go to e3."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "e4", PieceType.KNIGHT, Color.BLACK)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e3") in moves
        assert Position.from_algebraic("e4") not in moves


class TestPawnCaptures:
    """Pawn diagonal captures."""

    def test_white_pawn_captures_diagonally(self, empty_board, validator):
        """White pawn on e4 can capture on d5 and f5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e4", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "d5", PieceType.PAWN, Color.BLACK)
        place_piece(empty_board, "f5", PieceType.KNIGHT, Color.BLACK)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d5") in moves
        assert Position.from_algebraic("f5") in moves

    def test_white_pawn_cannot_capture_own_piece(self, empty_board, validator):
        """White pawn on e4 cannot capture own piece on d5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e4", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        place_piece(empty_board, "d5", PieceType.KNIGHT, Color.WHITE, has_moved=True)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d5") not in moves

    def test_black_pawn_captures_diagonally(self, empty_board, validator):
        """Black pawn on d5 can capture on c4 and e4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d5", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        place_piece(empty_board, "c4", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "e4", PieceType.PAWN, Color.WHITE)
        empty_board.current_turn = Color.BLACK

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("c4") in moves
        assert Position.from_algebraic("e4") in moves


class TestEnPassant:
    """En passant special capture."""

    def test_white_en_passant_capture(self, empty_board, validator):
        """White pawn on e5 can en passant capture black pawn that just double-moved to d5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        _, black_pawn = place_piece(
            empty_board, "d5", PieceType.PAWN, Color.BLACK, has_moved=True
        )

        # Simulate that black's last move was a double pawn push d7->d5
        last_move = Move(
            black_pawn,
            Position.from_algebraic("d7"),
            Position.from_algebraic("d5"),
        )
        empty_board.move_history.append(last_move)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d6") in moves

    def test_black_en_passant_capture(self, empty_board, validator):
        """Black pawn on d4 can en passant capture white pawn that just double-moved to e4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d4", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        _, white_pawn = place_piece(
            empty_board, "e4", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        empty_board.current_turn = Color.BLACK

        # Simulate that white's last move was a double pawn push e2->e4
        last_move = Move(
            white_pawn,
            Position.from_algebraic("e2"),
            Position.from_algebraic("e4"),
        )
        empty_board.move_history.append(last_move)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e3") in moves

    def test_en_passant_not_available_without_double_push(self, empty_board, validator):
        """En passant is not available if the last move wasn't a double pawn push."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        _, black_pawn = place_piece(
            empty_board, "d5", PieceType.PAWN, Color.BLACK, has_moved=True
        )

        # Simulate that black's last move was a single pawn push d6->d5 (not double)
        last_move = Move(
            black_pawn,
            Position.from_algebraic("d6"),
            Position.from_algebraic("d5"),
        )
        empty_board.move_history.append(last_move)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d6") not in moves

    def test_en_passant_not_available_if_not_adjacent(self, empty_board, validator):
        """En passant is not available if the pawn is not adjacent to the double-pushed pawn."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        _, black_pawn = place_piece(
            empty_board, "g5", PieceType.PAWN, Color.BLACK, has_moved=True
        )

        # Black double-pushed g7->g5, but white pawn on e5 is not adjacent
        last_move = Move(
            black_pawn,
            Position.from_algebraic("g7"),
            Position.from_algebraic("g5"),
        )
        empty_board.move_history.append(last_move)

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("g6") not in moves


class TestPawnPromotion:
    """Pawn reaching the back rank."""

    def test_white_pawn_can_reach_promotion_rank(self, empty_board, validator):
        """White pawn on e7 has e8 as a legal move (reaching promotion rank)."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "e7", PieceType.PAWN, Color.WHITE, has_moved=True
        )

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("e8") in moves

    def test_black_pawn_can_reach_promotion_rank(self, empty_board, validator):
        """Black pawn on d2 has d1 as a legal move (reaching promotion rank)."""
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        pos, _ = place_piece(
            empty_board, "d2", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        empty_board.current_turn = Color.BLACK

        moves = set(validator.get_legal_moves(empty_board, pos))
        assert Position.from_algebraic("d1") in moves
