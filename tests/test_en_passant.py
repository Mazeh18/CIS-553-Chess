"""Tests for en passant: legality, board execution, and undo."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.move import Move
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from tests.conftest import place_piece

# ── Helpers ──────────────────────────────────────────────────────────────


def _add_double_push_to_history(board, color, col):
    """Simulate a double-pawn-push by placing the pawn and adding a Move to history.

    For black: pawn goes from row 1 to row 3 (ranks 7 -> 5).
    For white: pawn goes from row 6 to row 4 (ranks 2 -> 4).
    """
    if color == Color.BLACK:
        start_row, end_row = 1, 3
    else:
        start_row, end_row = 6, 4

    pawn = Piece(PieceType.PAWN, color, has_moved=True)
    end_pos = Position(end_row, col)
    board.set_piece(end_pos, pawn)

    history_move = Move(
        piece=pawn,
        start_pos=Position(start_row, col),
        end_pos=end_pos,
    )
    board.move_history.append(history_move)
    return pawn


# ── Valid en passant ─────────────────────────────────────────────────────


class TestWhiteEnPassant:
    def test_valid_en_passant_left(self, empty_board, validator):
        """White pawn on e5 can capture black pawn that just double-pushed to d5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        # White pawn on e5 (row 3, col 4)
        wp_pos, _ = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        # Black pawn double-pushes to d5 (row 3, col 3)
        _add_double_push_to_history(empty_board, Color.BLACK, 3)

        legal = validator.get_legal_moves(empty_board, wp_pos)
        # En passant target: d6 = Position(2, 3)
        assert Position(2, 3) in legal

    def test_valid_en_passant_right(self, empty_board, validator):
        """White pawn on e5 can capture black pawn that just double-pushed to f5."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        wp_pos, _ = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        _add_double_push_to_history(empty_board, Color.BLACK, 5)  # f5

        legal = validator.get_legal_moves(empty_board, wp_pos)
        assert Position(2, 5) in legal  # f6


class TestBlackEnPassant:
    def test_valid_en_passant(self, empty_board, validator):
        """Black pawn on d4 can capture white pawn that just double-pushed to e4."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        # Black pawn on d4 (row 4, col 3)
        bp_pos, _ = place_piece(
            empty_board, "d4", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        # White pawn double-pushes to e4 (row 4, col 4)
        _add_double_push_to_history(empty_board, Color.WHITE, 4)

        empty_board.current_turn = Color.BLACK
        legal = validator.get_legal_moves(empty_board, bp_pos)
        # En passant target: e3 = Position(5, 4)
        assert Position(5, 4) in legal


# ── Invalid en passant ───────────────────────────────────────────────────


class TestEnPassantInvalid:
    def test_last_move_not_double_push(self, empty_board, validator):
        """En passant disallowed when last move was a single pawn push."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        wp_pos, _ = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        # Place black pawn at d5 with a single-square push in history
        bp = Piece(PieceType.PAWN, Color.BLACK, has_moved=True)
        empty_board.set_piece(Position(3, 3), bp)
        single_push = Move(
            piece=bp,
            start_pos=Position(2, 3),  # d6
            end_pos=Position(3, 3),  # d5
        )
        empty_board.move_history.append(single_push)

        legal = validator.get_legal_moves(empty_board, wp_pos)
        # d6 should NOT be in legal moves as en passant
        # Normal capture of d5 would go to (2, 3) only if diagonal, but
        # since there is a piece at d5, diagonal capture IS possible.
        # The en passant target d6 = Position(2, 3) is the diagonal capture, but
        # that square has the pawn that just moved from there... let's check
        # that en passant specifically is not triggered by verifying the logic:
        # Actually, d5 has a black pawn so exd6 is not en passant -- exd5 is a
        # regular diagonal capture. The key is that Position(2, 3) = d6 should
        # not appear as a move target.
        assert Position(2, 3) not in legal

    def test_pawn_not_on_correct_rank(self, empty_board, validator):
        """En passant only works from the 5th rank (white) or 4th rank (black)."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        # White pawn on e4 (row 4) -- NOT on 5th rank (row 3)
        wp_pos, _ = place_piece(
            empty_board, "e4", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        # Black pawn double-pushes to d4
        _add_double_push_to_history(empty_board, Color.BLACK, 3)

        legal = validator.get_legal_moves(empty_board, wp_pos)
        # d3 = Position(5, 3) should not be available via en passant
        # because white pawn is on row 4, not row 3
        assert Position(5, 3) not in legal

    def test_pawn_not_adjacent(self, empty_board, validator):
        """En passant only works when pawns are on adjacent columns."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        # White pawn on b5 (row 3, col 1)
        wp_pos, _ = place_piece(
            empty_board, "b5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        # Black pawn double-pushes to d5 (col 3) -- two columns away
        _add_double_push_to_history(empty_board, Color.BLACK, 3)

        legal = validator.get_legal_moves(empty_board, wp_pos)
        # d6 = Position(2, 3) should not be reachable
        assert Position(2, 3) not in legal


# ── Board execution ──────────────────────────────────────────────────────


class TestEnPassantExecution:
    def test_captured_pawn_removed(self, empty_board):
        """After en passant, the captured pawn is removed from the board."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        wp_pos, wp = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        bp = _add_double_push_to_history(empty_board, Color.BLACK, 3)  # d5

        ep_target = Position(2, 3)  # d6
        move = Move(
            piece=wp,
            start_pos=wp_pos,
            end_pos=ep_target,
            captured_piece=bp,
            is_en_passant=True,
        )
        empty_board.execute_move(move)

        # Capturing pawn is now at d6
        assert empty_board.get_piece(ep_target) is wp
        # Original position empty
        assert empty_board.get_piece(wp_pos) is None
        # Captured pawn at d5 removed
        assert empty_board.get_piece(Position(3, 3)) is None

    def test_black_en_passant_execution(self, empty_board):
        """Black en passant removes white pawn correctly."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        bp_pos, bp = place_piece(
            empty_board, "d4", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        wp = _add_double_push_to_history(empty_board, Color.WHITE, 4)  # e4

        ep_target = Position(5, 4)  # e3
        move = Move(
            piece=bp,
            start_pos=bp_pos,
            end_pos=ep_target,
            captured_piece=wp,
            is_en_passant=True,
        )
        empty_board.execute_move(move)

        assert empty_board.get_piece(ep_target) is bp
        assert empty_board.get_piece(bp_pos) is None
        assert empty_board.get_piece(Position(4, 4)) is None  # e4 cleared


# ── Undo ─────────────────────────────────────────────────────────────────


class TestEnPassantUndo:
    def test_undo_restores_both_pawns(self, empty_board):
        """Undoing en passant restores both the capturing and captured pawns."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        wp_pos, wp = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        bp = _add_double_push_to_history(empty_board, Color.BLACK, 3)  # d5
        captured_pawn_pos = Position(3, 3)  # d5

        ep_target = Position(2, 3)  # d6
        move = Move(
            piece=wp,
            start_pos=wp_pos,
            end_pos=ep_target,
            captured_piece=bp,
            is_en_passant=True,
        )
        empty_board.execute_move(move)
        empty_board.undo_move()

        # White pawn restored to e5
        assert empty_board.get_piece(wp_pos) is wp
        # Black pawn restored to d5
        assert empty_board.get_piece(captured_pawn_pos) is bp
        # d6 is empty again
        assert empty_board.get_piece(ep_target) is None

    def test_undo_black_en_passant(self, empty_board):
        """Undoing black en passant restores both pawns."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=True)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK, has_moved=True)

        bp_pos, bp = place_piece(
            empty_board, "d4", PieceType.PAWN, Color.BLACK, has_moved=True
        )
        wp = _add_double_push_to_history(empty_board, Color.WHITE, 4)  # e4
        captured_pawn_pos = Position(4, 4)  # e4

        ep_target = Position(5, 4)  # e3
        move = Move(
            piece=bp,
            start_pos=bp_pos,
            end_pos=ep_target,
            captured_piece=wp,
            is_en_passant=True,
        )
        empty_board.execute_move(move)
        empty_board.undo_move()

        assert empty_board.get_piece(bp_pos) is bp
        assert empty_board.get_piece(captured_pawn_pos) is wp
        assert empty_board.get_piece(ep_target) is None
