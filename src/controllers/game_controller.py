from typing import Optional

from src.entities.board import Board
from src.entities.position import Position
from src.entities.move import Move
from src.entities.move_result import MoveResult
from src.entities.move_attempt import MoveAttempt
from src.entities.game_state import GameState
from src.entities.time_control import TimeControl
from src.entities.enums import Color, GameStatus
from src.controllers.move_validator import MoveValidator
from src.controllers.notation_controller import NotationController


class GameController:
    """Central orchestrator for the game. Owns GameState, dispatches actions."""

    def __init__(self) -> None:
        self._move_validator = MoveValidator()
        self._notation_controller = NotationController()
        self.game_state: Optional[GameState] = None

    def new_game(self, time_control: TimeControl) -> None:
        """Initialize a new game with the given time control."""
        board = Board()
        board.initialize_standard()
        self.game_state = GameState(board, time_control)

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
        if captured_piece is not None:
            self.game_state.captured_pieces.add_captured(captured_piece)

        # Create Move and execute
        move = Move(
            piece=piece,
            start_pos=attempt.start_pos,
            end_pos=attempt.end_pos,
            captured_piece=captured_piece,
        )
        board.execute_move(move)

        # Generate notation
        move.notation = self._notation_controller.generate_notation(board, move)

        # Switch turn
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

    def get_legal_moves(self, position: Position) -> list[Position]:
        """Get legal destinations for the piece at the given position."""
        if self.game_state is None:
            return []
        return self._move_validator.get_legal_moves(self.game_state.board, position)

    def update(self, delta: float) -> None:
        """Called each frame. Clock updates will go here in the future."""
        pass

    def resign(self, color: Color) -> None:
        """End the game by resignation."""
        if self.game_state:
            self.game_state.status = GameStatus.RESIGNED
            self.game_state.winner = color.opposite()

    def undo_last_move(self) -> None:
        """Stub for future undo functionality."""
        pass

    def _check_post_move_status(self, board: Board, color_to_move: Color) -> GameStatus:
        """Check for check, checkmate, stalemate after a move."""
        in_check = self._move_validator.is_in_check(board, color_to_move)

        if in_check:
            if self._move_validator.is_checkmate(board, color_to_move):
                return GameStatus.CHECKMATE
            return GameStatus.CHECK

        if self._move_validator.is_stalemate(board, color_to_move):
            return GameStatus.STALEMATE

        # Draw detection stubbed for future: DrawDetector.check_draw_conditions(board)

        return GameStatus.ACTIVE
