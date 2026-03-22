"""Tests for algebraic notation generation."""

import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.move import Move
from src.entities.enums import Color, PieceType
from src.controllers.notation_controller import NotationController
from tests.conftest import place_piece


@pytest.fixture
def notation():
    """Return a NotationController instance."""
    return NotationController()


class TestPawnNotation:
    """Tests for pawn move notation."""

    def test_normal_pawn_move(self, empty_board, notation):
        """A simple pawn push is written as the destination square, e.g. 'e4'."""
        _pos, pawn = place_piece(empty_board, "e2", PieceType.PAWN, Color.WHITE)
        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e2"),
            end_pos=Position.from_algebraic("e4"),
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "e4"

    def test_pawn_capture(self, empty_board, notation):
        """A pawn capture is written as file + 'x' + destination, e.g. 'exd5'."""
        _pos, pawn = place_piece(empty_board, "e4", PieceType.PAWN, Color.WHITE)
        _pos, captured = place_piece(empty_board, "d5", PieceType.PAWN, Color.BLACK)
        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e4"),
            end_pos=Position.from_algebraic("d5"),
            captured_piece=captured,
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "exd5"


class TestPieceNotation:
    """Tests for non-pawn piece notation."""

    def test_knight_move(self, empty_board, notation):
        """A knight move is 'N' + destination, e.g. 'Nf3'."""
        _pos, knight = place_piece(empty_board, "g1", PieceType.KNIGHT, Color.WHITE)
        move = Move(
            piece=knight,
            start_pos=Position.from_algebraic("g1"),
            end_pos=Position.from_algebraic("f3"),
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "Nf3"

    def test_bishop_capture(self, empty_board, notation):
        """A bishop capture is 'Bx' + destination, e.g. 'Bxe5'."""
        _pos, bishop = place_piece(empty_board, "c3", PieceType.BISHOP, Color.WHITE)
        _pos, captured = place_piece(empty_board, "e5", PieceType.PAWN, Color.BLACK)
        move = Move(
            piece=bishop,
            start_pos=Position.from_algebraic("c3"),
            end_pos=Position.from_algebraic("e5"),
            captured_piece=captured,
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "Bxe5"


class TestCastlingNotation:
    """Tests for castling notation."""

    def test_kingside_castling(self, empty_board, notation):
        """Kingside castling is written as 'O-O'."""
        _pos, king = place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        move = Move(
            piece=king,
            start_pos=Position.from_algebraic("e1"),
            end_pos=Position.from_algebraic("g1"),
            is_castling=True,
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "O-O"

    def test_queenside_castling(self, empty_board, notation):
        """Queenside castling is written as 'O-O-O'."""
        _pos, king = place_piece(empty_board, "e1", PieceType.KING, Color.WHITE)
        move = Move(
            piece=king,
            start_pos=Position.from_algebraic("e1"),
            end_pos=Position.from_algebraic("c1"),
            is_castling=True,
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "O-O-O"


class TestPromotionNotation:
    """Tests for pawn promotion notation."""

    def test_promotion_to_queen(self, empty_board, notation):
        """Promotion is destination + '=' + piece letter, e.g. 'e8=Q'."""
        _pos, pawn = place_piece(empty_board, "e7", PieceType.PAWN, Color.WHITE)
        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e7"),
            end_pos=Position.from_algebraic("e8"),
            promotion_piece=PieceType.QUEEN,
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "e8=Q"

    def test_promotion_with_capture(self, empty_board, notation):
        """Promotion via capture includes file and 'x', e.g. 'exd8=Q'."""
        _pos, pawn = place_piece(empty_board, "e7", PieceType.PAWN, Color.WHITE)
        _pos, captured = place_piece(empty_board, "d8", PieceType.ROOK, Color.BLACK)
        move = Move(
            piece=pawn,
            start_pos=Position.from_algebraic("e7"),
            end_pos=Position.from_algebraic("d8"),
            captured_piece=captured,
            promotion_piece=PieceType.QUEEN,
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "exd8=Q"


class TestDisambiguation:
    """Tests for move disambiguation when multiple same-type pieces can reach the target."""

    def test_disambiguation_by_file(self, empty_board, notation):
        """Two rooks on the same rank: disambiguate by file letter."""
        # Rook on a1 and rook on h1, both can reach d1
        _pos, rook_a = place_piece(empty_board, "a1", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "h1", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "e3", PieceType.KING, Color.WHITE)

        move = Move(
            piece=rook_a,
            start_pos=Position.from_algebraic("a1"),
            end_pos=Position.from_algebraic("d1"),
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "Rad1"

    def test_disambiguation_by_rank(self, empty_board, notation):
        """Two rooks on the same file: disambiguate by rank number."""
        # Rook on a1 and rook on a8, both can reach a4
        _pos, rook_1 = place_piece(empty_board, "a1", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "a8", PieceType.ROOK, Color.WHITE)
        place_piece(empty_board, "e3", PieceType.KING, Color.WHITE)

        move = Move(
            piece=rook_1,
            start_pos=Position.from_algebraic("a1"),
            end_pos=Position.from_algebraic("a4"),
        )

        result = notation.generate_notation(empty_board, move)
        assert result == "R1a4"
