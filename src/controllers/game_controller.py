from typing import Optional

from src.entities.board import Board
from src.entities.position import Position
from src.entities.piece import Piece
from src.entities.move import Move
from src.entities.move_result import MoveResult
from src.entities.move_attempt import MoveAttempt
from src.entities.game_state import GameState
from src.entities.time_control import TimeControl
from src.entities.enums import Color, GameStatus, PieceType
from src.controllers.move_validator import MoveValidator
from src.controllers.notation_controller import NotationController
from src.controllers.draw_detector import DrawDetector
from src.controllers.clock_controller import ClockController

class GameController:
    """Central orchestrator for the game. Owns GameState, dispatches actions."""

    def __init__(self) -> None:
        self._move_validator = MoveValidator()
        self._notation_controller = NotationController()
        self._draw_detector = DrawDetector()
        self._clock_controller = ClockController()
        self.game_state: Optional[GameState] = None

    def new_game(self, time_control: TimeControl) -> None:
        """Initialize a new game with the given time control."""
        board = Board()
        board.initialize_standard()
        self.game_state = GameState(board, time_control)
        self._clock_controller.clock = self.game_state.clock
        self._clock_controller.initialize(time_control)
        self._clock_controller.start_clock(Color.WHITE)

    def attempt_move(self, attempt: MoveAttempt) -> MoveResult:
        """Validate and execute a move. Returns MoveResult."""
        if self.game_state is None or self.game_state.is_game_over():
            return MoveResult(
                success=False,
                is_promotion=False,
                new_status=(
                    self.game_state.status if self.game_state else GameStatus.ACTIVE
                ),
            )

        board = self.game_state.board

        # Validate the move
        legal_moves = self._move_validator.get_legal_moves(board, attempt.start_pos)
        if attempt.end_pos not in legal_moves:
            return MoveResult(
                success=False,
                is_promotion=False,
                new_status=self.game_state.status,
            )

        piece = board.get_piece(attempt.start_pos)
        if piece is None:
            return MoveResult(
                success=False,
                is_promotion=False,
                new_status=self.game_state.status,
            )

        # Check for capture
        captured_piece = board.get_piece(attempt.end_pos)

        # Detect en passant
        is_en_passant = False
        if (
            piece.piece_type == PieceType.PAWN
            and captured_piece is None
            and attempt.start_pos.col != attempt.end_pos.col
        ):
            is_en_passant = True
            captured_pawn_pos = Position(attempt.start_pos.row, attempt.end_pos.col)
            captured_piece = board.get_piece(captured_pawn_pos)

        # Detect castling
        is_castling = (
            piece.piece_type == PieceType.KING
            and abs(attempt.start_pos.col - attempt.end_pos.col) == 2
        )

        # Track captured piece
        if captured_piece is not None:
            self.game_state.captured_pieces.add_captured(captured_piece)

        # Create Move and execute
        move = Move(
            piece=piece,
            start_pos=attempt.start_pos,
            end_pos=attempt.end_pos,
            captured_piece=captured_piece,
            is_castling=is_castling,
            is_en_passant=is_en_passant,
            time_after_move=self._clock_controller.clock.get_time(board.current_turn)
        )
        board.execute_move(move)

        # Detect promotion
        promotion_row = 0 if piece.color == Color.WHITE else 7
        if piece.piece_type == PieceType.PAWN and attempt.end_pos.row == promotion_row:
            self.game_state.pending_promotion = attempt.end_pos
            self._clock_controller.stop_clock()
            return MoveResult(
                success=True,
                is_promotion=True,
                new_status=self.game_state.status,
            )

        # Generate notation
        move.notation = self._notation_controller.generate_notation(board, move)

        # Switch turn
        self._clock_controller.switch_turn(board.current_turn)
        board.switch_turn()

        # Post-move status checks
        opponent = board.current_turn
        new_status = self._check_post_move_status(board, opponent)

        # Append check/checkmate symbol to notation
        if new_status == GameStatus.CHECK:
            move.notation += "+"
        elif new_status == GameStatus.CHECKMATE:
            move.notation += "#"

        # Update game state
        self.game_state.status = new_status
        if new_status == GameStatus.CHECKMATE:
            self.game_state.winner = opponent.opposite()

        return MoveResult(
            success=True,
            is_promotion=False,
            new_status=new_status,
        )

    def attempt_promotion(self, piece_type: PieceType) -> MoveResult:
        """Complete a pending pawn promotion."""
        if self.game_state is None or self.game_state.pending_promotion is None:
            return MoveResult(
                success=False,
                is_promotion=False,
                new_status=(
                    self.game_state.status if self.game_state else GameStatus.ACTIVE
                ),
            )

        pos = self.game_state.pending_promotion
        board = self.game_state.board
        pawn = board.get_piece(pos)

        # Replace pawn with promoted piece
        promoted = Piece(piece_type, pawn.color, has_moved=True)
        board.set_piece(pos, promoted)

        # Update the last move's promotion_piece
        last_move = board.move_history[-1]
        last_move.promotion_piece = piece_type

        # Generate notation (now with promotion info)
        last_move.notation = self._notation_controller.generate_notation(
            board, last_move
        )

        # Switch turn
        self._clock_controller.switch_turn(board.current_turn)
        board.switch_turn()

        # Clear pending promotion
        self.game_state.pending_promotion = None

        # Post-move status checks
        opponent = board.current_turn
        new_status = self._check_post_move_status(board, opponent)

        # Append check/checkmate symbol to notation
        if new_status == GameStatus.CHECK:
            last_move.notation += "+"
        elif new_status == GameStatus.CHECKMATE:
            last_move.notation += "#"

        # Update game state
        self.game_state.status = new_status
        if new_status == GameStatus.CHECKMATE:
            self.game_state.winner = opponent.opposite()

        return MoveResult(
            success=True,
            is_promotion=False,
            new_status=new_status,
        )

    def get_legal_moves(self, position: Position) -> list[Position]:
        """Get legal destinations for the piece at the given position."""
        if self.game_state is None:
            return []
        return self._move_validator.get_legal_moves(self.game_state.board, position)

    def update(self, delta: float) -> None:
        """Called each frame. Clock updates will go here in the future."""
        if self._clock_controller.update(delta):
            self.game_state.status = GameStatus.TIMEOUT
            board = self.game_state.board
            self.game_state.winner = board.current_turn.opposite()
            self._clock_controller.stop_clock()

    def resign(self, color: Color) -> None:
        """End the game by resignation."""
        if self.game_state:
            self.game_state.status = GameStatus.RESIGNED
            self.game_state.winner = color.opposite()
            self._clock_controller.stop_clock()

    def undo_last_move(self) -> bool:
        """Revert the last move on the board, restore captured pieces, recalculate status.

        Returns True if a move was undone, False if there was nothing to undo.
        """
        if self.game_state is None:
            return False

        board = self.game_state.board
        if not board.move_history:
            return False

        # Cannot undo during a pending promotion
        if self.game_state.pending_promotion is not None:
            return False

        move = board.undo_move()
        if move is None:
            return False

        # Restore captured piece to CapturedPieces tracker
        if move.captured_piece is not None:
            # The capturing color is the piece that moved
            capturing_color = move.piece.color
            self.game_state.captured_pieces.remove_last_captured(capturing_color)

        # Recalculate game status
        current_color = board.current_turn
        if current_color == Color.WHITE:
            self._clock_controller.clock.white_time = move.time_after_move
        else:
            self._clock_controller.clock.black_time = move.time_after_move

        if self._move_validator.is_in_check(board, current_color):
            self.game_state.status = GameStatus.CHECK
        else:
            self.game_state.status = GameStatus.ACTIVE

        # Clear any game-over state
        self.game_state.winner = None

        return True

    def _check_post_move_status(self, board: Board, color_to_move: Color) -> GameStatus:
        """Check for check, checkmate, stalemate after a move."""
        in_check = self._move_validator.is_in_check(board, color_to_move)

        if in_check:
            if self._move_validator.is_checkmate(board, color_to_move):
                self._clock_controller.stop_clock()
                return GameStatus.CHECKMATE
            return GameStatus.CHECK

        if self._move_validator.is_stalemate(board, color_to_move):
            self._clock_controller.stop_clock()
            return GameStatus.STALEMATE

        draw_status = self._draw_detector.check_draw_conditions(board)
        if draw_status is not None:
            self._clock_controller.stop_clock()
            return draw_status

        return GameStatus.ACTIVE
