from src.entities.board import Board
from src.entities.move import Move
from src.entities.enums import PieceType

PIECE_LETTERS = {
    PieceType.KING: "K",
    PieceType.QUEEN: "Q",
    PieceType.ROOK: "R",
    PieceType.BISHOP: "B",
    PieceType.KNIGHT: "N",
    PieceType.PAWN: "",
}


class NotationController:
    """Stateless controller for generating standard algebraic notation."""

    def generate_notation(self, board: Board, move: Move) -> str:
        """Produce the algebraic notation string for a move (e.g., 'Nf3', 'exd5')."""
        piece_letter = PIECE_LETTERS[move.piece.piece_type]
        dest = move.end_pos.to_algebraic()
        capture = "x" if move.captured_piece is not None else ""

        if move.piece.piece_type == PieceType.PAWN:
            if move.captured_piece is not None:
                # Pawn captures use file letter: e.g., exd5
                file_letter = chr(ord("a") + move.start_pos.col)
                return f"{file_letter}x{dest}"
            else:
                return dest
        else:
            disambiguation = self.needs_disambiguation(board, move)
            return f"{piece_letter}{disambiguation}{capture}{dest}"

    def needs_disambiguation(self, board: Board, move: Move) -> str:
        """Return disambiguation string when multiple pieces of the same type can reach the target."""
        if move.piece.piece_type in (PieceType.PAWN, PieceType.KING):
            return ""

        # Find other pieces of the same type and color that can also reach the target
        ambiguous = []
        for pos, piece in board.get_pieces_by_color(move.piece.color):
            if (
                piece.piece_type == move.piece.piece_type
                and pos != move.start_pos
                and pos != move.end_pos  # Exclude the piece that just moved
            ):
                # Check if this piece can also reach the destination
                # (We check raw reachability, not full legality, which is standard for notation)
                if self._can_reach(board, pos, move.end_pos, piece):
                    ambiguous.append(pos)

        if not ambiguous:
            return ""

        # Check if file is sufficient
        same_file = any(p.col == move.start_pos.col for p in ambiguous)
        same_rank = any(p.row == move.start_pos.row for p in ambiguous)

        if not same_file:
            return chr(ord("a") + move.start_pos.col)
        elif not same_rank:
            return str(8 - move.start_pos.row)
        else:
            return move.start_pos.to_algebraic()

    def _can_reach(self, board: Board, from_pos, to_pos, piece) -> bool:
        """Simple reachability check for disambiguation purposes."""
        dr = to_pos.row - from_pos.row
        dc = to_pos.col - from_pos.col

        if piece.piece_type == PieceType.KNIGHT:
            return (abs(dr), abs(dc)) in ((1, 2), (2, 1))

        if piece.piece_type == PieceType.ROOK:
            return dr == 0 or dc == 0

        if piece.piece_type == PieceType.BISHOP:
            return abs(dr) == abs(dc) and dr != 0

        if piece.piece_type == PieceType.QUEEN:
            return dr == 0 or dc == 0 or abs(dr) == abs(dc)

        return False
