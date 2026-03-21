"""Tests for pawn promotion via GameController: all piece choices, capture, and notation."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.move import Move
from src.entities.move_attempt import MoveAttempt
from src.entities.move_result import MoveResult
from src.entities.enums import Color, PieceType, GameStatus
from src.entities.time_control import TimeControl
from src.controllers.game_controller import GameController
from tests.conftest import place_piece

# ── Helpers ──────────────────────────────────────────────────────────────


def _setup_promotion_game():
    """Return a GameController with a minimal board: white pawn on 7th rank ready to promote.

    Board layout:
      - White king on e1
      - Black king on e8
      - White pawn on a7 (row 1, col 0) -- one step from promotion
    Turn: White
    """
    gc = GameController()
    tc = TimeControl("No Time", None, 0)
    gc.new_game(tc)

    # Clear the board and set up a minimal position
    board = gc.game_state.board
    board.squares = [[None for _ in range(8)] for _ in range(8)]
    board.current_turn = Color.WHITE
    board.move_history = []
    board.position_history = []
    board.halfmove_clock = 0

    place_piece(board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
    place_piece(board, "e8", PieceType.KING, Color.BLACK, has_moved=True)
    place_piece(board, "a7", PieceType.PAWN, Color.WHITE, has_moved=True)

    return gc


def _setup_promotion_with_capture():
    """White pawn on a7, black rook on b8 -- promotion with capture."""
    gc = _setup_promotion_game()
    board = gc.game_state.board
    place_piece(board, "b8", PieceType.ROOK, Color.BLACK, has_moved=True)
    return gc


# ── Basic promotion flow ─────────────────────────────────────────────────


class TestPromotionFlow:
    def test_move_returns_is_promotion(self):
        """Moving a pawn to the last rank returns is_promotion=True."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        result = gc.attempt_move(MoveAttempt(start, end))

        assert result.success is True
        assert result.is_promotion is True

    def test_pending_promotion_set(self):
        """Game state has pending_promotion after pawn reaches last rank."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))

        assert gc.game_state.pending_promotion == Position.from_algebraic("a8")

    def test_promote_to_queen(self):
        """Promoting to queen replaces pawn with queen on the board."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))

        result = gc.attempt_promotion(PieceType.QUEEN)
        assert result.success is True

        piece = gc.game_state.board.get_piece(Position.from_algebraic("a8"))
        assert piece is not None
        assert piece.piece_type == PieceType.QUEEN
        assert piece.color == Color.WHITE

    def test_pending_promotion_cleared(self):
        """pending_promotion is cleared after successful promotion."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.QUEEN)

        assert gc.game_state.pending_promotion is None

    def test_turn_switches_after_promotion(self):
        """Turn switches to black after white completes promotion."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.QUEEN)

        assert gc.game_state.board.current_turn == Color.BLACK


# ── All promotion piece choices ──────────────────────────────────────────


class TestPromotionChoices:
    @pytest.mark.parametrize(
        "piece_type",
        [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT],
    )
    def test_promote_to_each_piece(self, piece_type):
        """Pawn can be promoted to queen, rook, bishop, or knight."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))

        result = gc.attempt_promotion(piece_type)
        assert result.success is True

        piece = gc.game_state.board.get_piece(Position.from_algebraic("a8"))
        assert piece.piece_type == piece_type
        assert piece.color == Color.WHITE


# ── Promotion with capture ───────────────────────────────────────────────


class TestPromotionCapture:
    def test_capture_promotion(self):
        """Pawn captures diagonally onto the last rank and promotes."""
        gc = _setup_promotion_with_capture()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("b8")  # capture the black rook
        result = gc.attempt_move(MoveAttempt(start, end))

        assert result.success is True
        assert result.is_promotion is True

        result = gc.attempt_promotion(PieceType.QUEEN)
        assert result.success is True

        piece = gc.game_state.board.get_piece(Position.from_algebraic("b8"))
        assert piece.piece_type == PieceType.QUEEN
        assert piece.color == Color.WHITE

    def test_captured_piece_tracked(self):
        """The captured piece is recorded in game_state.captured_pieces."""
        gc = _setup_promotion_with_capture()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("b8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.QUEEN)

        # The captured rook should be in captured_pieces
        last_move = gc.game_state.board.move_history[-1]
        assert last_move.captured_piece is not None
        assert last_move.captured_piece.piece_type == PieceType.ROOK


# ── Notation ─────────────────────────────────────────────────────────────


class TestPromotionNotation:
    def test_queen_promotion_notation(self):
        """Notation includes =Q for queen promotion."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.QUEEN)

        last_move = gc.game_state.board.move_history[-1]
        assert "=Q" in last_move.notation

    def test_rook_promotion_notation(self):
        """Notation includes =R for rook promotion."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.ROOK)

        last_move = gc.game_state.board.move_history[-1]
        assert "=R" in last_move.notation

    def test_bishop_promotion_notation(self):
        """Notation includes =B for bishop promotion."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.BISHOP)

        last_move = gc.game_state.board.move_history[-1]
        assert "=B" in last_move.notation

    def test_knight_promotion_notation(self):
        """Notation includes =N for knight promotion."""
        gc = _setup_promotion_game()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("a8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.KNIGHT)

        last_move = gc.game_state.board.move_history[-1]
        assert "=N" in last_move.notation

    def test_capture_promotion_notation(self):
        """Capture promotion notation includes both capture and promotion suffix."""
        gc = _setup_promotion_with_capture()
        start = Position.from_algebraic("a7")
        end = Position.from_algebraic("b8")
        gc.attempt_move(MoveAttempt(start, end))
        gc.attempt_promotion(PieceType.QUEEN)

        last_move = gc.game_state.board.move_history[-1]
        # Should contain capture indicator and promotion: e.g., "axb8=Q"
        assert "x" in last_move.notation
        assert "=Q" in last_move.notation
