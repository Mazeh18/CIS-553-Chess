from typing import Optional

from src.entities.enums import Color, GameStatus
from src.entities.board import Board
from src.entities.position import Position
from src.entities.time_control import TimeControl
from src.entities.captured_pieces import CapturedPieces
from src.entities.clock import Clock


class GameState:
    """Top-level game container composing Board, TimeControl, and CapturedPieces."""

    def __init__(self, board: Board, time_control: TimeControl) -> None:
        self.status: GameStatus = GameStatus.ACTIVE
        self.winner: Optional[Color] = None
        self.board: Board = board
        self.clock = Clock()
        self.time_control: TimeControl = time_control
        self.captured_pieces: CapturedPieces = CapturedPieces()
        self.pending_promotion: Optional[Position] = None

    def is_game_over(self) -> bool:
        """Return True if the game has ended."""
        return self.status.is_game_over()

    def get_result_message(self) -> str:
        """Return a human-readable result string."""
        if self.status == GameStatus.CHECKMATE:
            winner_name = self.winner.name.capitalize() if self.winner else "Unknown"
            return f"Checkmate! {winner_name} wins."
        elif self.status == GameStatus.STALEMATE:
            return "Stalemate! The game is a draw."
        elif self.status == GameStatus.RESIGNED:
            winner_name = self.winner.name.capitalize() if self.winner else "Unknown"
            loser = self.winner.opposite() if self.winner else None
            loser_name = loser.name.capitalize() if loser else "Unknown"
            return f"{loser_name} resigned. {winner_name} wins!"
        elif self.status == GameStatus.TIMEOUT:
            winner_name = self.winner.name.capitalize() if self.winner else "Unknown"
            return f"Time expired! {winner_name} wins."
        elif self.status.is_draw():
            return "The game is a draw."
        elif self.status == GameStatus.CHECK:
            return "Check!"
        else:
            return ""
