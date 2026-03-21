"""Tests for castling logic: legality, board execution, undo, and notation."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.move import Move
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from src.controllers.notation_controller import NotationController
from tests.conftest import place_piece

# ── Helper ───────────────────────────────────────────────────────────────


def _setup_castling_board(board, color):
    """Place king and both rooks on an empty board for castling tests.

    Also places the opposite-color king so find_king never raises.
    Returns (king_pos, king_piece).
    """
    back_rank = 7 if color == Color.WHITE else 0
    opp_rank = 0 if color == Color.WHITE else 7

    king_pos, king = place_piece(
        board, f"e{8 - back_rank}", PieceType.KING, color, has_moved=False
    )
    place_piece(board, f"a{8 - back_rank}", PieceType.ROOK, color, has_moved=False)
    place_piece(board, f"h{8 - back_rank}", PieceType.ROOK, color, has_moved=False)
    # Opposite king tucked away
    place_piece(
        board, f"a{8 - opp_rank}", PieceType.KING, color.opposite(), has_moved=True
    )

    # Set the correct turn
    board.current_turn = color
    return king_pos, king


# ── White castling legality ──────────────────────────────────────────────


class TestWhiteKingsideCastling:
    def test_kingside_in_legal_moves(self, empty_board, validator):
        king_pos, _ = _setup_castling_board(empty_board, Color.WHITE)
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) in legal  # g1

    def test_queenside_in_legal_moves(self, empty_board, validator):
        king_pos, _ = _setup_castling_board(empty_board, Color.WHITE)
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 2) in legal  # c1


class TestBlackCastling:
    def test_kingside_in_legal_moves(self, empty_board, validator):
        king_pos, _ = _setup_castling_board(empty_board, Color.BLACK)
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(0, 6) in legal  # g8

    def test_queenside_in_legal_moves(self, empty_board, validator):
        king_pos, _ = _setup_castling_board(empty_board, Color.BLACK)
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(0, 2) in legal  # c8


# ── Invalid castling scenarios ───────────────────────────────────────────


class TestCastlingInvalid:
    def test_king_has_moved(self, empty_board, validator):
        """Castling disallowed when king has already moved."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE, has_moved=False)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        king_pos = Position.from_algebraic("e1")
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) not in legal

    def test_rook_has_moved(self, empty_board, validator):
        """Castling disallowed when the rook has already moved."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=False)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE, has_moved=True)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        king_pos = Position.from_algebraic("e1")
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) not in legal

    def test_piece_between_king_and_rook_kingside(self, empty_board, validator):
        """Castling blocked when a piece sits between king and rook."""
        king_pos, _ = _setup_castling_board(empty_board, Color.WHITE)
        place_piece(empty_board, "f1", PieceType.BISHOP, Color.WHITE, has_moved=True)
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) not in legal

    def test_piece_between_king_and_rook_queenside(self, empty_board, validator):
        """Castling blocked on queenside when a piece sits between."""
        king_pos, _ = _setup_castling_board(empty_board, Color.WHITE)
        place_piece(empty_board, "b1", PieceType.KNIGHT, Color.WHITE, has_moved=True)
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 2) not in legal

    def test_king_in_check(self, empty_board, validator):
        """Castling disallowed while in check."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=False)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE, has_moved=False)
        place_piece(empty_board, "a1", PieceType.ROOK, Color.WHITE, has_moved=False)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        # Black rook attacks e1
        place_piece(empty_board, "e8", PieceType.ROOK, Color.BLACK, has_moved=True)
        king_pos = Position.from_algebraic("e1")
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) not in legal
        assert Position(7, 2) not in legal

    def test_king_passes_through_attacked_square(self, empty_board, validator):
        """Castling disallowed when king passes through attacked square (f1)."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=False)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE, has_moved=False)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        # Black rook attacks f1
        place_piece(empty_board, "f8", PieceType.ROOK, Color.BLACK, has_moved=True)
        king_pos = Position.from_algebraic("e1")
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) not in legal

    def test_king_lands_on_attacked_square(self, empty_board, validator):
        """Castling disallowed when destination square (g1) is attacked."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=False)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE, has_moved=False)
        place_piece(empty_board, "a8", PieceType.KING, Color.BLACK, has_moved=True)
        # Black rook attacks g1
        place_piece(empty_board, "g8", PieceType.ROOK, Color.BLACK, has_moved=True)
        king_pos = Position.from_algebraic("e1")
        legal = validator.get_legal_moves(empty_board, king_pos)
        assert Position(7, 6) not in legal


# ── Board execution and undo ─────────────────────────────────────────────


class TestCastlingExecution:
    def test_kingside_execution(self, empty_board):
        """After kingside castling, king is at g1 and rook at f1."""
        king_pos, king = _setup_castling_board(empty_board, Color.WHITE)
        rook = empty_board.get_piece(Position(7, 7))

        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(7, 6),
            is_castling=True,
        )
        empty_board.execute_move(move)

        assert empty_board.get_piece(Position(7, 6)) is king  # king at g1
        assert empty_board.get_piece(Position(7, 5)) is rook  # rook at f1
        assert empty_board.get_piece(Position(7, 4)) is None  # e1 empty
        assert empty_board.get_piece(Position(7, 7)) is None  # h1 empty

    def test_queenside_execution(self, empty_board):
        """After queenside castling, king is at c1 and rook at d1."""
        king_pos, king = _setup_castling_board(empty_board, Color.WHITE)
        rook = empty_board.get_piece(Position(7, 0))

        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(7, 2),
            is_castling=True,
        )
        empty_board.execute_move(move)

        assert empty_board.get_piece(Position(7, 2)) is king  # king at c1
        assert empty_board.get_piece(Position(7, 3)) is rook  # rook at d1
        assert empty_board.get_piece(Position(7, 4)) is None  # e1 empty
        assert empty_board.get_piece(Position(7, 0)) is None  # a1 empty

    def test_black_kingside_execution(self, empty_board):
        """After black kingside castling, king at g8 and rook at f8."""
        king_pos, king = _setup_castling_board(empty_board, Color.BLACK)
        rook = empty_board.get_piece(Position(0, 7))

        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(0, 6),
            is_castling=True,
        )
        empty_board.execute_move(move)

        assert empty_board.get_piece(Position(0, 6)) is king
        assert empty_board.get_piece(Position(0, 5)) is rook
        assert empty_board.get_piece(Position(0, 4)) is None
        assert empty_board.get_piece(Position(0, 7)) is None

    def test_black_queenside_execution(self, empty_board):
        """After black queenside castling, king at c8 and rook at d8."""
        king_pos, king = _setup_castling_board(empty_board, Color.BLACK)
        rook = empty_board.get_piece(Position(0, 0))

        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(0, 2),
            is_castling=True,
        )
        empty_board.execute_move(move)

        assert empty_board.get_piece(Position(0, 2)) is king
        assert empty_board.get_piece(Position(0, 3)) is rook
        assert empty_board.get_piece(Position(0, 4)) is None
        assert empty_board.get_piece(Position(0, 0)) is None


class TestCastlingUndo:
    def test_undo_kingside(self, empty_board):
        """Undo restores king and rook to original squares."""
        king_pos, king = _setup_castling_board(empty_board, Color.WHITE)
        rook = empty_board.get_piece(Position(7, 7))

        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(7, 6),
            is_castling=True,
        )
        empty_board.execute_move(move)
        empty_board.undo_move()

        assert empty_board.get_piece(Position(7, 4)) is king  # king back at e1
        assert empty_board.get_piece(Position(7, 7)) is rook  # rook back at h1
        assert empty_board.get_piece(Position(7, 6)) is None
        assert empty_board.get_piece(Position(7, 5)) is None
        assert not king.has_moved
        assert not rook.has_moved

    def test_undo_queenside(self, empty_board):
        """Undo restores king and rook to original squares (queenside)."""
        king_pos, king = _setup_castling_board(empty_board, Color.WHITE)
        rook = empty_board.get_piece(Position(7, 0))

        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(7, 2),
            is_castling=True,
        )
        empty_board.execute_move(move)
        empty_board.undo_move()

        assert empty_board.get_piece(Position(7, 4)) is king
        assert empty_board.get_piece(Position(7, 0)) is rook
        assert empty_board.get_piece(Position(7, 2)) is None
        assert empty_board.get_piece(Position(7, 3)) is None
        assert not king.has_moved
        assert not rook.has_moved


# ── Notation ─────────────────────────────────────────────────────────────


class TestCastlingNotation:
    def test_kingside_notation(self, empty_board):
        """Kingside castling notation is O-O."""
        king_pos, king = _setup_castling_board(empty_board, Color.WHITE)
        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(7, 6),
            is_castling=True,
        )
        notation_ctrl = NotationController()
        notation = notation_ctrl.generate_notation(empty_board, move)
        assert notation == "O-O"

    def test_queenside_notation(self, empty_board):
        """Queenside castling notation is O-O-O."""
        king_pos, king = _setup_castling_board(empty_board, Color.WHITE)
        move = Move(
            piece=king,
            start_pos=king_pos,
            end_pos=Position(7, 2),
            is_castling=True,
        )
        notation_ctrl = NotationController()
        notation = notation_ctrl.generate_notation(empty_board, move)
        assert notation == "O-O-O"
