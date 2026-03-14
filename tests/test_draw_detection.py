"""Tests for draw condition detection."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.enums import Color, PieceType, GameStatus
from src.controllers.draw_detector import DrawDetector
from tests.conftest import place_piece


class TestInsufficientMaterial:
    """Tests for DrawDetector.is_insufficient_material."""

    def test_king_vs_king(self, empty_board, draw_detector):
        """K vs K is insufficient material."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        assert draw_detector.is_insufficient_material(empty_board) is True

    def test_king_bishop_vs_king(self, empty_board, draw_detector):
        """K+B vs K is insufficient material."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "c1", PieceType.BISHOP, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        assert draw_detector.is_insufficient_material(empty_board) is True

    def test_king_knight_vs_king(self, empty_board, draw_detector):
        """K+N vs K is insufficient material."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "b1", PieceType.KNIGHT, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        assert draw_detector.is_insufficient_material(empty_board) is True

    def test_king_bishop_vs_king_bishop_same_color_squares(
        self, empty_board, draw_detector
    ):
        """K+B vs K+B with same-color-square bishops is insufficient material."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        # c1 is (7,2), sum=9 (odd) -> dark square
        place_piece(empty_board, "c1", PieceType.BISHOP, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)
        # f8 is (0,5), sum=5 (odd) -> dark square (same color)
        place_piece(empty_board, "f8", PieceType.BISHOP, Color.BLACK)

        assert draw_detector.is_insufficient_material(empty_board) is True

    def test_king_bishop_vs_king_bishop_different_color_squares(
        self, empty_board, draw_detector
    ):
        """K+B vs K+B with different-color-square bishops is NOT insufficient."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        # c1 is (7,2), sum=9 (odd) -> dark square
        place_piece(empty_board, "c1", PieceType.BISHOP, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)
        # c8 is (0,2), sum=2 (even) -> light square (different color)
        place_piece(empty_board, "c8", PieceType.BISHOP, Color.BLACK)

        assert draw_detector.is_insufficient_material(empty_board) is False

    def test_king_queen_vs_king_not_insufficient(self, empty_board, draw_detector):
        """K+Q vs K is NOT insufficient material."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "d1", PieceType.QUEEN, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        assert draw_detector.is_insufficient_material(empty_board) is False


class TestThreefoldRepetition:
    """Tests for DrawDetector.is_threefold_repetition."""

    def test_threefold_repetition_detected(self, empty_board, draw_detector):
        """Position occurring 3 times triggers threefold repetition."""
        pos_hash = "some_position_hash"
        empty_board.position_history = [pos_hash, "other", pos_hash, "other2", pos_hash]

        assert draw_detector.is_threefold_repetition(empty_board) is True

    def test_not_threefold_with_two_occurrences(self, empty_board, draw_detector):
        """Only 2 occurrences of the same position is not threefold."""
        pos_hash = "some_position_hash"
        empty_board.position_history = [pos_hash, "other", pos_hash]

        assert draw_detector.is_threefold_repetition(empty_board) is False

    def test_empty_position_history(self, empty_board, draw_detector):
        """Empty position history should not trigger threefold."""
        empty_board.position_history = []

        assert draw_detector.is_threefold_repetition(empty_board) is False


class TestFiftyMoveRule:
    """Tests for DrawDetector.is_fifty_move_rule."""

    def test_fifty_move_rule_triggered(self, empty_board, draw_detector):
        """Halfmove clock at 100 triggers the fifty-move rule."""
        empty_board.halfmove_clock = 100

        assert draw_detector.is_fifty_move_rule(empty_board) is True

    def test_fifty_move_rule_not_triggered(self, empty_board, draw_detector):
        """Halfmove clock at 99 does not trigger the fifty-move rule."""
        empty_board.halfmove_clock = 99

        assert draw_detector.is_fifty_move_rule(empty_board) is False

    def test_fifty_move_rule_above_100(self, empty_board, draw_detector):
        """Halfmove clock above 100 also triggers the rule."""
        empty_board.halfmove_clock = 150

        assert draw_detector.is_fifty_move_rule(empty_board) is True


class TestCheckDrawConditions:
    """Tests for DrawDetector.check_draw_conditions."""

    def test_returns_insufficient_material(self, empty_board, draw_detector):
        """check_draw_conditions returns DRAW_INSUFFICIENT_MATERIAL for K vs K."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        result = draw_detector.check_draw_conditions(empty_board)
        assert result == GameStatus.DRAW_INSUFFICIENT_MATERIAL

    def test_returns_fifty_move(self, empty_board, draw_detector):
        """check_draw_conditions returns DRAW_FIFTY_MOVE when clock hits 100."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)
        place_piece(empty_board, "a1", PieceType.ROOK, Color.WHITE)
        empty_board.halfmove_clock = 100
        # Need position_history to avoid insufficient material taking priority
        # Actually K+R vs K is not insufficient, so it won't match that
        empty_board.position_history = ["hash1"]

        result = draw_detector.check_draw_conditions(empty_board)
        assert result == GameStatus.DRAW_FIFTY_MOVE

    def test_returns_threefold_repetition(self, empty_board, draw_detector):
        """check_draw_conditions returns DRAW_THREEFOLD_REPETITION."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)
        place_piece(empty_board, "a1", PieceType.ROOK, Color.WHITE)
        pos_hash = "repeated_hash"
        empty_board.position_history = [pos_hash, "x", pos_hash, "y", pos_hash]

        result = draw_detector.check_draw_conditions(empty_board)
        assert result == GameStatus.DRAW_THREEFOLD_REPETITION

    def test_returns_none_when_no_draw(self, empty_board, draw_detector):
        """check_draw_conditions returns None when no draw condition is met."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)
        place_piece(empty_board, "a1", PieceType.ROOK, Color.WHITE)
        empty_board.halfmove_clock = 0
        empty_board.position_history = ["unique_hash"]

        result = draw_detector.check_draw_conditions(empty_board)
        assert result is None
