import pytest

from src.entities.board import Board
from src.entities.piece import Piece
from src.entities.position import Position
from src.entities.enums import Color, PieceType
from src.controllers.move_validator import MoveValidator
from src.controllers.draw_detector import DrawDetector


def place_piece(board, algebraic, piece_type, color, has_moved=False):
    """Place a piece on the board at the given algebraic position."""
    pos = Position.from_algebraic(algebraic)
    piece = Piece(piece_type, color, has_moved=has_moved)
    board.set_piece(pos, piece)
    return pos, piece


@pytest.fixture
def empty_board():
    """Return an empty Board (no pieces)."""
    return Board()


@pytest.fixture
def standard_board():
    """Return a Board with the standard starting position."""
    board = Board()
    board.initialize_standard()
    return board


@pytest.fixture
def validator():
    """Return a MoveValidator instance."""
    return MoveValidator()


@pytest.fixture
def draw_detector():
    """Return a DrawDetector instance."""
    return DrawDetector()
