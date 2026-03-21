from src.entities.board import Board
from src.entities.position import Position
from src.entities.piece import Piece
from src.entities.enums import Color, PieceType


class MoveValidator:
    """Stateless chess move legality checker."""

    def get_legal_moves(self, board: Board, position: Position) -> list[Position]:
        """Return all legal destination squares for the piece at the given position."""
        piece = board.get_piece(position)
        if piece is None:
            return []
        raw_moves = self._get_raw_moves(board, position, piece)
        return self._filter_check_moves(board, position, raw_moves, piece.color)

    def is_in_check(self, board: Board, color: Color) -> bool:
        """Return whether the given color's king is currently in check."""
        king_pos = board.find_king(color)
        return self.is_square_attacked(board, king_pos, color.opposite())

    def is_checkmate(self, board: Board, color: Color) -> bool:
        """Return whether the given color is in checkmate."""
        if not self.is_in_check(board, color):
            return False
        return self._has_no_legal_moves(board, color)

    def is_stalemate(self, board: Board, color: Color) -> bool:
        """Return whether the given color is in stalemate."""
        if self.is_in_check(board, color):
            return False
        return self._has_no_legal_moves(board, color)

    def is_square_attacked(
        self, board: Board, position: Position, by_color: Color
    ) -> bool:
        """Return whether the given square is attacked by any piece of the specified color."""
        for pos, piece in board.get_pieces_by_color(by_color):
            if piece.piece_type == PieceType.PAWN:
                attacks = self._get_pawn_attacks(board, pos, piece)
            elif piece.piece_type == PieceType.KING:
                attacks = self._get_king_attacks(pos)
            else:
                attacks = self._get_raw_moves(board, pos, piece)
            if position in attacks:
                return True
        return False

    # ── Private helpers ──────────────────────────────────────────────────

    def _has_no_legal_moves(self, board: Board, color: Color) -> bool:
        """Return True if the given color has no legal moves at all."""
        for pos, _piece in board.get_pieces_by_color(color):
            if self.get_legal_moves(board, pos):
                return False
        return True

    def _get_raw_moves(
        self, board: Board, position: Position, piece: Piece
    ) -> list[Position]:
        """Get raw candidate moves for a piece (before check filtering)."""
        dispatch = {
            PieceType.PAWN: self._get_pawn_moves,
            PieceType.ROOK: self._get_rook_moves,
            PieceType.BISHOP: self._get_bishop_moves,
            PieceType.QUEEN: self._get_queen_moves,
            PieceType.KING: self._get_king_moves,
            PieceType.KNIGHT: self._get_knight_moves,
        }
        return dispatch[piece.piece_type](board, position, piece)

    def _get_pawn_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Pawn moves: forward, double from start, diagonal captures, en passant."""
        moves = []
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # One square forward
        one_ahead = Position(pos.row + direction, pos.col)
        if one_ahead.is_valid() and board.get_piece(one_ahead) is None:
            moves.append(one_ahead)
            # Two squares forward from starting rank
            if pos.row == start_row:
                two_ahead = Position(pos.row + 2 * direction, pos.col)
                if two_ahead.is_valid() and board.get_piece(two_ahead) is None:
                    moves.append(two_ahead)

        # Diagonal captures
        for dcol in (-1, 1):
            target_pos = Position(pos.row + direction, pos.col + dcol)
            if target_pos.is_valid():
                target_piece = board.get_piece(target_pos)
                if target_piece is not None and target_piece.color != piece.color:
                    moves.append(target_pos)

        # En passant
        if board.move_history:
            last_move = board.move_history[-1]
            if (
                last_move.piece.piece_type == PieceType.PAWN
                and abs(last_move.start_pos.row - last_move.end_pos.row) == 2
            ):
                en_passant_row = 3 if piece.color == Color.WHITE else 4
                if pos.row == en_passant_row:
                    if abs(pos.col - last_move.end_pos.col) == 1:
                        ep_target = Position(pos.row + direction, last_move.end_pos.col)
                        moves.append(ep_target)

        return moves

    def _get_king_attacks(self, pos: Position) -> list[Position]:
        """Return squares a king attacks (all 8 adjacent), regardless of occupancy."""
        attacks = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                target = Position(pos.row + dr, pos.col + dc)
                if target.is_valid():
                    attacks.append(target)
        return attacks

    def _get_pawn_attacks(
        self, _board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Return squares a pawn attacks (diagonals only), regardless of occupancy."""
        direction = -1 if piece.color == Color.WHITE else 1
        attacks = []
        for dcol in (-1, 1):
            target = Position(pos.row + direction, pos.col + dcol)
            if target.is_valid():
                attacks.append(target)
        return attacks

    def _get_rook_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Rook: horizontal and vertical sliding."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return self._get_sliding_moves(board, pos, directions, piece.color)

    def _get_bishop_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Bishop: diagonal sliding."""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._get_sliding_moves(board, pos, directions, piece.color)

    def _get_queen_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Queen: combines rook + bishop moves."""
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        return self._get_sliding_moves(board, pos, directions, piece.color)

    def _get_king_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """King: one square in any direction, plus castling."""
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                target = Position(pos.row + dr, pos.col + dc)
                if target.is_valid():
                    occupant = board.get_piece(target)
                    if occupant is None or occupant.color != piece.color:
                        moves.append(target)

        moves.extend(self._get_castling_moves(board, pos, piece))

        return moves

    def _get_castling_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Kingside and queenside castling with all precondition checks."""
        moves = []
        if piece.has_moved:
            return moves
        if self.is_in_check(board, piece.color):
            return moves

        back_rank = 7 if piece.color == Color.WHITE else 0
        opp = piece.color.opposite()

        # Kingside: rook at col 7, king moves to col 6
        rook_ks = board.get_piece(Position(back_rank, 7))
        if (
            rook_ks is not None
            and rook_ks.piece_type == PieceType.ROOK
            and rook_ks.color == piece.color
            and not rook_ks.has_moved
        ):
            if (
                board.get_piece(Position(back_rank, 5)) is None
                and board.get_piece(Position(back_rank, 6)) is None
            ):
                if not self.is_square_attacked(
                    board, Position(back_rank, 5), opp
                ) and not self.is_square_attacked(board, Position(back_rank, 6), opp):
                    moves.append(Position(back_rank, 6))

        # Queenside: rook at col 0, king moves to col 2
        rook_qs = board.get_piece(Position(back_rank, 0))
        if (
            rook_qs is not None
            and rook_qs.piece_type == PieceType.ROOK
            and rook_qs.color == piece.color
            and not rook_qs.has_moved
        ):
            if (
                board.get_piece(Position(back_rank, 1)) is None
                and board.get_piece(Position(back_rank, 2)) is None
                and board.get_piece(Position(back_rank, 3)) is None
            ):
                if not self.is_square_attacked(
                    board, Position(back_rank, 2), opp
                ) and not self.is_square_attacked(board, Position(back_rank, 3), opp):
                    moves.append(Position(back_rank, 2))

        return moves

    def _get_knight_moves(
        self, board: Board, pos: Position, piece: Piece
    ) -> list[Position]:
        """Knight: L-shaped jumps, can skip over pieces."""
        moves = []
        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dr, dc in offsets:
            target = Position(pos.row + dr, pos.col + dc)
            if target.is_valid():
                occupant = board.get_piece(target)
                if occupant is None or occupant.color != piece.color:
                    moves.append(target)
        return moves

    def _get_sliding_moves(
        self,
        board: Board,
        pos: Position,
        directions: list[tuple],
        color: Color,
    ) -> list[Position]:
        """Shared helper for sliding pieces (rook, bishop, queen)."""
        moves = []
        for dr, dc in directions:
            r, c = pos.row + dr, pos.col + dc
            while 0 <= r <= 7 and 0 <= c <= 7:
                target = Position(r, c)
                occupant = board.get_piece(target)
                if occupant is None:
                    moves.append(target)
                elif occupant.color != color:
                    moves.append(target)  # capture
                    break
                else:
                    break  # blocked by own piece
                r += dr
                c += dc
        return moves

    def _filter_check_moves(
        self,
        board: Board,
        position: Position,
        moves: list[Position],
        color: Color,
    ) -> list[Position]:
        """Remove moves that would leave the own king in check."""
        legal = []
        for target in moves:
            # Clone the board and simulate the move
            test_board = board.clone()
            piece = test_board.get_piece(position)
            test_board.set_piece(target, piece)
            test_board.set_piece(position, None)

            # En passant: also remove the captured pawn
            if (
                piece.piece_type == PieceType.PAWN
                and position.col != target.col
                and board.get_piece(target) is None
            ):
                captured_pawn_pos = Position(position.row, target.col)
                test_board.set_piece(captured_pawn_pos, None)

            # Castling: also move the rook
            if (
                piece.piece_type == PieceType.KING
                and abs(position.col - target.col) == 2
            ):
                if target.col == 6:  # kingside
                    rook_from = Position(position.row, 7)
                    rook_to = Position(position.row, 5)
                else:  # queenside
                    rook_from = Position(position.row, 0)
                    rook_to = Position(position.row, 3)
                rook = test_board.get_piece(rook_from)
                test_board.set_piece(rook_to, rook)
                test_board.set_piece(rook_from, None)

            # Check if own king is still safe
            king_pos = test_board.find_king(color)
            if not self._is_square_attacked_on_board(
                test_board, king_pos, color.opposite()
            ):
                legal.append(target)
        return legal

    def _is_square_attacked_on_board(
        self, board: Board, position: Position, by_color: Color
    ) -> bool:
        """Check if a square is attacked on a given board (used for check filtering)."""
        for pos, piece in board.get_pieces_by_color(by_color):
            if piece.piece_type == PieceType.PAWN:
                attacks = self._get_pawn_attacks(board, pos, piece)
            elif piece.piece_type == PieceType.KING:
                attacks = self._get_king_attacks(pos)
            else:
                attacks = self._get_raw_moves(board, pos, piece)
            if position in attacks:
                return True
        return False
