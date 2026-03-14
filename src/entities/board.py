import copy
from typing import Optional

from src.entities.enums import Color, PieceType
from src.entities.position import Position
from src.entities.piece import Piece
from src.entities.move import Move


class Board:
    """The 8x8 game board with pieces, turn tracking, and move history."""

    def __init__(self) -> None:
        self.squares: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.current_turn: Color = Color.WHITE
        self.move_history: list[Move] = []
        self.halfmove_clock: int = 0
        self.fullmove_number: int = 1
        self.position_history: list[str] = []

    def initialize_standard(self) -> None:
        """Set up the standard starting position with 32 pieces."""
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.move_history = []
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.position_history = []

        back_rank = [
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]

        # Black back rank (row 0 = rank 8)
        for col, pt in enumerate(back_rank):
            self.squares[0][col] = Piece(pt, Color.BLACK)
        # Black pawns (row 1 = rank 7)
        for col in range(8):
            self.squares[1][col] = Piece(PieceType.PAWN, Color.BLACK)

        # White pawns (row 6 = rank 2)
        for col in range(8):
            self.squares[6][col] = Piece(PieceType.PAWN, Color.WHITE)
        # White back rank (row 7 = rank 1)
        for col, pt in enumerate(back_rank):
            self.squares[7][col] = Piece(pt, Color.WHITE)

        self.position_history.append(self.get_position_hash())

    def get_piece(self, pos: Position) -> Optional[Piece]:
        """Return the piece at the given position, or None."""
        return self.squares[pos.row][pos.col]

    def set_piece(self, pos: Position, piece: Optional[Piece]) -> None:
        """Place a piece (or None) at the given position."""
        self.squares[pos.row][pos.col] = piece

    def execute_move(self, move: Move) -> None:
        """Execute a move on the board. Does NOT switch turn."""
        # Update halfmove clock
        if move.piece.piece_type == PieceType.PAWN or move.captured_piece is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Move the piece
        self.set_piece(move.end_pos, move.piece)
        self.set_piece(move.start_pos, None)
        move.piece.has_moved = True

        # En passant: remove the captured pawn
        if move.is_en_passant:
            captured_pawn_pos = Position(move.start_pos.row, move.end_pos.col)
            self.set_piece(captured_pawn_pos, None)

        # Castling: also move the rook
        if move.is_castling:
            if move.end_pos.col == 6:  # kingside
                rook_from = Position(move.start_pos.row, 7)
                rook_to = Position(move.start_pos.row, 5)
            else:  # queenside
                rook_from = Position(move.start_pos.row, 0)
                rook_to = Position(move.start_pos.row, 3)
            rook = self.get_piece(rook_from)
            self.set_piece(rook_to, rook)
            self.set_piece(rook_from, None)
            if rook:
                rook.has_moved = True

        # Promotion: replace pawn with promoted piece
        if move.promotion_piece is not None:
            promoted = Piece(move.promotion_piece, move.piece.color, has_moved=True)
            self.set_piece(move.end_pos, promoted)

        # Add move to history
        self.move_history.append(move)

        # Record position hash
        self.position_history.append(self.get_position_hash())

    def undo_move(self) -> Optional[Move]:
        """Undo the last move. Returns the undone Move, or None if no history."""
        if not self.move_history:
            return None

        move = self.move_history.pop()

        # Restore piece to start position
        self.set_piece(move.start_pos, move.piece)
        move.piece.has_moved = move.had_moved

        # Handle special move undo
        if move.is_en_passant:
            # Destination was empty; captured pawn was adjacent
            self.set_piece(move.end_pos, None)
            captured_pawn_pos = Position(move.start_pos.row, move.end_pos.col)
            self.set_piece(captured_pawn_pos, move.captured_piece)
        elif move.promotion_piece is not None:
            # Remove promoted piece, restore captured piece (if any)
            self.set_piece(move.end_pos, move.captured_piece)
        else:
            # Normal move: restore captured piece (or None) to end position
            self.set_piece(move.end_pos, move.captured_piece)

        # Castling: move rook back
        if move.is_castling:
            if move.end_pos.col == 6:  # kingside
                rook_from = Position(move.start_pos.row, 7)
                rook_to = Position(move.start_pos.row, 5)
            else:  # queenside
                rook_from = Position(move.start_pos.row, 0)
                rook_to = Position(move.start_pos.row, 3)
            rook = self.get_piece(rook_to)
            self.set_piece(rook_from, rook)
            self.set_piece(rook_to, None)
            if rook:
                rook.has_moved = False

        # Revert position history
        if self.position_history:
            self.position_history.pop()

        # Revert fullmove number
        if self.current_turn == Color.WHITE:
            self.fullmove_number -= 1

        # Switch turn back
        self.switch_turn()

        return move

    def switch_turn(self) -> None:
        """Switch the current turn to the other player."""
        if self.current_turn == Color.BLACK:
            self.fullmove_number += 1
        self.current_turn = self.current_turn.opposite()

    def get_position_hash(self) -> str:
        """Generate a hash string of the current board position for repetition detection."""
        parts = []
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece is not None:
                    parts.append(f"{row}{col}{piece.piece_type.name}{piece.color.name}")
        parts.append(self.current_turn.name)

        # Castling rights
        for row in (0, 7):
            king = self.squares[row][4]
            if king and king.piece_type == PieceType.KING and not king.has_moved:
                parts.append(f"CK{row}")
            for col in (0, 7):
                rook = self.squares[row][col]
                if rook and rook.piece_type == PieceType.ROOK and not rook.has_moved:
                    parts.append(f"CR{row}{col}")

        # En passant availability
        if self.move_history:
            last = self.move_history[-1]
            if (
                last.piece.piece_type == PieceType.PAWN
                and abs(last.start_pos.row - last.end_pos.row) == 2
            ):
                parts.append(f"EP{last.end_pos.col}")

        return "|".join(parts)

    def find_king(self, color: Color) -> Position:
        """Find and return the Position of the King of the given color."""
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if (
                    piece
                    and piece.piece_type == PieceType.KING
                    and piece.color == color
                ):
                    return Position(row, col)
        raise ValueError(f"No {color.name} king found on the board")

    def get_pieces_by_color(self, color: Color) -> list[tuple]:
        """Return all (Position, Piece) pairs for the given color."""
        result = []
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.color == color:
                    result.append((Position(row, col), piece))
        return result

    def clone(self) -> "Board":
        """Create a deep copy of this board for speculative move testing."""
        return copy.deepcopy(self)
