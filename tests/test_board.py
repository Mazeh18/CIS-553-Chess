"""Tests for Board operations: execute_move, undo_move, clone, and position hashing."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.move import Move
from src.entities.enums import Color, PieceType
from tests.conftest import place_piece


class TestExecuteMove:
    """Tests for Board.execute_move."""

    def test_execute_move_sets_has_moved(self, empty_board):
        """After executing a move, the piece's has_moved flag is True."""
        _pos, pawn = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        assert pawn.has_moved is False

        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e2"),
            end_pos=Position.from_algebraic("e4"),
        )
        empty_board.execute_move(move)

        assert pawn.has_moved is True
        assert empty_board.get_piece(Position.from_algebraic("e4")) is pawn
        assert empty_board.get_piece(Position.from_algebraic("e2")) is None

    def test_execute_castling_moves_king_and_rook(self, empty_board):
        """Kingside castling moves both king to g1 and rook from h1 to f1."""
        _pos, king = place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        _pos, rook = place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE)

        move = Move(
            piece=king,
            start_pos=Position.from_algebraic("e1"),
            end_pos=Position.from_algebraic("g1"),
            is_castling=True,
        )
        empty_board.execute_move(move)

        assert empty_board.get_piece(Position.from_algebraic("g1")) is king
        assert empty_board.get_piece(Position.from_algebraic("f1")) is rook
        assert empty_board.get_piece(Position.from_algebraic("e1")) is None
        assert empty_board.get_piece(Position.from_algebraic("h1")) is None
        assert king.has_moved is True
        assert rook.has_moved is True

    def test_execute_en_passant_removes_captured_pawn(self, empty_board):
        """En passant removes the captured pawn from its original square."""
        _pos, white_pawn = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        _pos, black_pawn = place_piece(
            empty_board, "d5", PieceType.PAWN, Color.BLACK, has_moved=True
        )

        move = Move(
            piece=white_pawn,
            start_pos=Position.from_algebraic("e5"),
            end_pos=Position.from_algebraic("d6"),
            captured_piece=black_pawn,
            is_en_passant=True,
        )
        empty_board.execute_move(move)

        # White pawn is now on d6
        assert empty_board.get_piece(Position.from_algebraic("d6")) is white_pawn
        # Black pawn on d5 is removed
        assert empty_board.get_piece(Position.from_algebraic("d5")) is None
        # Original square is empty
        assert empty_board.get_piece(Position.from_algebraic("e5")) is None

    def test_execute_promotion_replaces_pawn(self, empty_board):
        """Promotion replaces the pawn with the promoted piece type."""
        _pos, pawn = place_piece(empty_board, "e7", PieceType.PAWN, Color.WHITE)

        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e7"),
            end_pos=Position.from_algebraic("e8"),
            promotion_piece=PieceType.QUEEN,
        )
        empty_board.execute_move(move)

        promoted = empty_board.get_piece(Position.from_algebraic("e8"))
        assert promoted is not None
        assert promoted.piece_type == PieceType.QUEEN
        assert promoted.color == Color.WHITE
        assert empty_board.get_piece(Position.from_algebraic("e7")) is None


class TestUndoMove:
    """Tests for Board.undo_move."""

    def test_undo_move_reverts_has_moved(self, empty_board):
        """Undoing a move restores the piece's original has_moved state."""
        _pos, pawn = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        assert pawn.has_moved is False

        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e2"),
            end_pos=Position.from_algebraic("e4"),
        )
        empty_board.execute_move(move)
        assert pawn.has_moved is True

        empty_board.undo_move()
        assert pawn.has_moved is False
        assert empty_board.get_piece(Position.from_algebraic("e2")) is pawn
        assert empty_board.get_piece(Position.from_algebraic("e4")) is None

    def test_undo_castling_restores_both_pieces(self, empty_board):
        """Undoing castling puts both king and rook back."""
        _pos, king = place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        _pos, rook = place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE)

        move = Move(
            piece=king,
            start_pos=Position.from_algebraic("e1"),
            end_pos=Position.from_algebraic("g1"),
            is_castling=True,
        )
        empty_board.execute_move(move)
        empty_board.undo_move()

        assert empty_board.get_piece(Position.from_algebraic("e1")) is king
        assert empty_board.get_piece(Position.from_algebraic("h1")) is rook
        assert empty_board.get_piece(Position.from_algebraic("g1")) is None
        assert empty_board.get_piece(Position.from_algebraic("f1")) is None
        assert king.has_moved is False
        assert rook.has_moved is False

    def test_undo_en_passant_restores_captured_pawn(self, empty_board):
        """Undoing en passant restores the captured pawn to its square."""
        _pos, white_pawn = place_piece(
            empty_board, "e5", PieceType.PAWN, Color.WHITE, has_moved=True
        )
        _pos, black_pawn = place_piece(
            empty_board, "d5", PieceType.PAWN, Color.BLACK, has_moved=True
        )

        move = Move(
            piece=white_pawn,
            start_pos=Position.from_algebraic("e5"),
            end_pos=Position.from_algebraic("d6"),
            captured_piece=black_pawn,
            is_en_passant=True,
        )
        empty_board.execute_move(move)
        empty_board.undo_move()

        assert empty_board.get_piece(Position.from_algebraic("e5")) is white_pawn
        assert empty_board.get_piece(Position.from_algebraic("d5")) is black_pawn
        assert empty_board.get_piece(Position.from_algebraic("d6")) is None


class TestClone:
    """Tests for Board.clone."""

    def test_clone_produces_independent_copy(self, empty_board):
        """Modifying a clone does not affect the original board."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)

        cloned = empty_board.clone()

        # Modify the clone
        cloned.set_piece(Position.from_algebraic("e1"), None)
        cloned.set_piece(
            Position.from_algebraic("d1"),
            Piece(PieceType.QUEEN, Color.WHITE),
        )

        # Original is unaffected
        original_king = empty_board.get_piece(Position.from_algebraic("e1"))
        assert original_king is not None
        assert original_king.piece_type == PieceType.KING

        assert empty_board.get_piece(Position.from_algebraic("d1")) is None


class TestPositionHash:
    """Tests for Board.get_position_hash."""

    def test_hash_changes_when_piece_moves(self, empty_board):
        """Position hash differs after a piece moves."""
        _pos, pawn = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        hash_before = empty_board.get_position_hash()

        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e2"),
            end_pos=Position.from_algebraic("e4"),
        )
        empty_board.execute_move(move)
        empty_board.switch_turn()  # switch turn so hash reflects new state

        hash_after = empty_board.get_position_hash()
        assert hash_before != hash_after

    def test_hash_includes_castling_rights(self, empty_board):
        """Position hash differs based on whether king has moved (castling rights)."""
        place_piece(empty_board, "e1", PieceType.KING, Color.WHITE, has_moved=False)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE, has_moved=False)
        place_piece(empty_board, "e8", PieceType.KING, Color.BLACK)

        hash_with_castling = empty_board.get_position_hash()

        # Now mark the king as having moved (losing castling rights)
        king = empty_board.get_piece(Position.from_algebraic("e1"))
        king.has_moved = True

        hash_without_castling = empty_board.get_position_hash()

        assert hash_with_castling != hash_without_castling
