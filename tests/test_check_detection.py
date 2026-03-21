"""Tests for check, checkmate, and stalemate detection."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece


class TestIsInCheck:
    """Tests for MoveValidator.is_in_check."""

    def test_king_in_check_from_rook(self, empty_board, validator):
        """A rook on the same rank as the king delivers check."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.ROOK, Color.BLACK)

        assert validator.is_in_check(empty_board, Color.WHITE) is True

    def test_king_in_check_from_bishop(self, empty_board, validator):
        """A bishop on a diagonal delivers check."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "h4", PieceType.BISHOP, Color.BLACK)

        assert validator.is_in_check(empty_board, Color.WHITE) is True

    def test_king_in_check_from_knight(self, empty_board, validator):
        """A knight an L-shape away delivers check."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "f3", PieceType.KNIGHT, Color.BLACK)

        assert validator.is_in_check(empty_board, Color.WHITE) is True

    def test_king_in_check_from_pawn(self, empty_board, validator):
        """A pawn diagonally ahead of the king delivers check."""
        place_piece(empty_board, "e4", PieceType.KING, Color.WHITE)
        # Black pawn on d5 attacks e4 (black pawns attack downward-diagonally)
        place_piece(empty_board, "d5", PieceType.PAWN, Color.BLACK)

        assert validator.is_in_check(empty_board, Color.WHITE) is True

    def test_king_not_in_check(self, empty_board, validator):
        """King is safe when no enemy piece attacks its square."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.ROOK, Color.BLACK)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        assert validator.is_in_check(empty_board, Color.WHITE) is False


class TestCheckmate:
    """Tests for MoveValidator.is_checkmate."""

    def test_scholars_mate(self, empty_board, validator):
        """Scholar's mate: queen on f7 with bishop support, black king trapped."""
        # Standard scholar's mate position after 1.e4 e5 2.Bc4 Nc6 3.Qh5 Nf6 4.Qxf7#
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        place_piece(empty_board, "f7", PieceType.QUEEN, Color.WHITE)
        place_piece(empty_board, "c4", PieceType.BISHOP, Color.WHITE)
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        # Black pieces blocking escape routes
        place_piece(empty_board, "d8", PieceType.QUEEN, Color.BLACK)
        place_piece(empty_board, "d7", PieceType.PAWN, Color.BLACK)
        place_piece(empty_board, "f8", PieceType.BISHOP, Color.BLACK)
        place_piece(empty_board, "e7", PieceType.PAWN, Color.BLACK)

        assert validator.is_checkmate(empty_board, Color.BLACK) is True

    def test_back_rank_mate(self, empty_board, validator):
        """Back rank mate: king trapped behind own pawns, rook delivers check."""
        place_piece(empty_board, "g8", PieceType.KING, Color.BLACK)
        place_piece(empty_board, "f7", PieceType.PAWN, Color.BLACK)
        place_piece(empty_board, "g7", PieceType.PAWN, Color.BLACK)
        place_piece(empty_board, "h7", PieceType.PAWN, Color.BLACK)
        place_piece(empty_board, "a8", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)

        assert validator.is_checkmate(empty_board, Color.BLACK) is True

    def test_not_checkmate_when_can_escape(self, empty_board, validator):
        """King in check but has an escape square is not checkmate."""
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
        place_piece(empty_board, "e1", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "a1", PieceType.KING, Color.WHITE, has_moved=True)

        assert validator.is_in_check(empty_board, Color.BLACK) is True
        assert validator.is_checkmate(empty_board, Color.BLACK) is False


class TestStalemate:
    """Tests for MoveValidator.is_stalemate."""

    def test_stalemate_king_cornered(self, empty_board, validator):
        """Classic stalemate: black king on a8, white queen on b6, white king on c6."""
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        place_piece(empty_board, "b6", PieceType.QUEEN, Color.WHITE)
        place_piece(empty_board, "c6", PieceType.KING, Color.WHITE, has_moved=True)

        assert validator.is_stalemate(empty_board, Color.BLACK) is True

    def test_not_stalemate_when_in_check(self, empty_board, validator):
        """If the king is in check it cannot be stalemate."""
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        place_piece(empty_board, "a6", PieceType.QUEEN, Color.WHITE)
        place_piece(empty_board, "c6", PieceType.KING, Color.WHITE, has_moved=True)

        assert validator.is_in_check(empty_board, Color.BLACK) is True
        assert validator.is_stalemate(empty_board, Color.BLACK) is False


class TestKingMoveLegality:
    """Tests that king movement respects check constraints."""

    def test_king_cannot_move_into_check(self, empty_board, validator):
        """Legal moves for king must exclude squares attacked by opponent."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "f8", PieceType.ROOK, Color.BLACK)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)

        king_pos = Position.from_algebraic("e1")
        legal = validator.get_legal_moves(empty_board, king_pos)

        # f1 and f2 are attacked by the rook on f8; king should not move there
        f1 = Position.from_algebraic("f1")
        f2 = Position.from_algebraic("f2")
        assert f1 not in legal
        assert f2 not in legal

    def test_must_escape_check(self, empty_board, validator):
        """When in check, only moves that resolve check are legal."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.ROOK, Color.BLACK)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        # Place a white pawn that cannot block or capture the rook
        place_piece(empty_board, "a2", PieceType.PAWN, Color.WHITE)

        assert validator.is_in_check(empty_board, Color.WHITE) is True

        # The pawn on a2 should have no legal moves because it cannot resolve check
        pawn_pos = Position.from_algebraic("a2")
        pawn_legal = validator.get_legal_moves(empty_board, pawn_pos)
        assert pawn_legal == []

        # The king should still have moves (away from the file)
        king_pos = Position.from_algebraic("e1")
        king_legal = validator.get_legal_moves(empty_board, king_pos)
        assert len(king_legal) > 0
        # All king legal moves must be off the e-file (rook controls it)
        for move_pos in king_legal:
            assert move_pos.col != 4  # col 4 = e-file
