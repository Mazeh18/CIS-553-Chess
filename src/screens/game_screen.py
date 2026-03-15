from typing import Callable, Optional

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.entities.enums import Color, PieceType, GameStatus
from src.entities.drag_state import DragState
from src.controllers.game_controller import GameController
from src.controllers.input_controller import InputController
from src.constants import (
    COLOR_BACKGROUND,
    COLOR_LIGHT_SQUARE,
    COLOR_DARK_SQUARE,
    COLOR_TEXT,
    COLOR_LABEL,
    COLOR_HIGHLIGHT_ORIGIN,
    FONT_NAME,
    FONT_SIZE_SMALL,
    FONT_SIZE_BODY,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# ── Piece rendering ────────────────────────────────────────────────────
PIECE_LETTER = {
    PieceType.KING: "K",
    PieceType.QUEEN: "Q",
    PieceType.ROOK: "R",
    PieceType.BISHOP: "B",
    PieceType.KNIGHT: "N",
    PieceType.PAWN: "P",
}

COLOR_WHITE_PIECE = (255, 255, 255)
COLOR_BLACK_PIECE = (30, 30, 30)
COLOR_WHITE_PIECE_TEXT = (30, 30, 30)
COLOR_BLACK_PIECE_TEXT = (220, 220, 220)

FILE_LABELS = "abcdefgh"
RANK_LABELS = "87654321"


class GameScreen(BaseScreen):
    """Game screen with interactive drag-and-drop chess."""

    def __init__(
        self,
        surface: pygame.Surface,
        game_controller: GameController,
        on_back: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(surface)
        self._game_controller = game_controller

        screen_w, screen_h = surface.get_size()

        # Board sizing: fit to ~85% of screen height, centered
        board_margin = 40
        self._square_size = (screen_h - board_margin * 2) // 8
        self._board_size = self._square_size * 8

        self._board_x = (screen_w - self._board_size) // 2
        self._board_y = (screen_h - self._board_size) // 2

        # Fonts
        self._label_font = pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL)
        self._piece_font = pygame.font.Font(FONT_NAME, int(self._square_size * 0.45))
        self._status_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)

        # Back button (top-left corner)
        self._back_button = Button(
            label="Main Menu",
            rect=pygame.Rect(20, 20, BUTTON_WIDTH, BUTTON_HEIGHT),
            on_click=on_back,
        )

        # Pre-render static board surface (squares + labels)
        self._board_surface = self._render_board()

        # Pre-render piece surfaces keyed by (PieceType, Color)
        self._piece_surfaces = self._render_pieces()

        # Drag-and-drop state and input controller
        self._drag_state = DragState()
        self._input_controller = InputController(
            drag_state=self._drag_state,
            board_x=self._board_x,
            board_y=self._board_y,
            square_size=self._square_size,
            get_legal_moves_fn=self._game_controller.get_legal_moves,
            get_current_turn_fn=self._get_current_turn,
        )

    def _get_current_turn(self) -> Color:
        """Return the color whose turn it is."""
        return self._game_controller.game_state.board.current_turn

    def _render_board(self) -> pygame.Surface:
        """Draw the 8x8 board with rank/file labels onto a surface."""
        sq = self._square_size
        surf = pygame.Surface((self._board_size, self._board_size))

        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = COLOR_LIGHT_SQUARE if is_light else COLOR_DARK_SQUARE
                pygame.draw.rect(surf, color, (col * sq, row * sq, sq, sq))

        # File labels (a-h) along the bottom
        for col in range(8):
            label = self._label_font.render(FILE_LABELS[col], True, COLOR_LABEL)
            surf.blit(
                label,
                (
                    col * sq + sq - label.get_width() - 2,
                    7 * sq + sq - label.get_height() - 1,
                ),
            )

        # Rank labels (8-1) along the left
        for row in range(8):
            label = self._label_font.render(RANK_LABELS[row], True, COLOR_LABEL)
            surf.blit(label, (2, row * sq + 1))

        return surf

    def _render_pieces(self) -> dict:
        """Pre-render placeholder piece surfaces (circle + letter)."""
        sq = self._square_size
        radius = int(sq * 0.38)
        surfaces = {}

        for piece_type in PieceType:
            for color in Color:
                piece_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)

                circle_color = (
                    COLOR_WHITE_PIECE if color == Color.WHITE else COLOR_BLACK_PIECE
                )
                pygame.draw.circle(piece_surf, circle_color, (sq // 2, sq // 2), radius)
                border_color = (180, 180, 180) if color == Color.WHITE else (80, 80, 80)
                pygame.draw.circle(
                    piece_surf, border_color, (sq // 2, sq // 2), radius, 2
                )

                text_color = (
                    COLOR_WHITE_PIECE_TEXT
                    if color == Color.WHITE
                    else COLOR_BLACK_PIECE_TEXT
                )
                letter_surf = self._piece_font.render(
                    PIECE_LETTER[piece_type], True, text_color
                )
                letter_rect = letter_surf.get_rect(center=(sq // 2, sq // 2))
                piece_surf.blit(letter_surf, letter_rect)

                surfaces[(piece_type, color)] = piece_surf

        return surfaces

    def handle_event(self, event: pygame.event.Event) -> None:
        self._back_button.handle_event(event)

        # No interaction during game over
        if self._game_controller.game_state.is_game_over():
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._input_controller.handle_mouse_down(
                event.pos, self._game_controller.game_state.board
            )
        elif event.type == pygame.MOUSEMOTION:
            self._input_controller.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            attempt = self._input_controller.handle_mouse_up(event.pos)
            if attempt is not None:
                self._game_controller.attempt_move(attempt)

    def update(self, dt: float) -> None:
        self._game_controller.update(dt)

    def draw(self) -> None:
        self.surface.fill(COLOR_BACKGROUND)

        # Board background
        self.surface.blit(self._board_surface, (self._board_x, self._board_y))

        # Highlight origin square and legal moves if dragging
        if self._drag_state.is_dragging:
            self._draw_highlights()

        # Pieces from the board entity
        sq = self._square_size
        board = self._game_controller.game_state.board
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece is not None:
                    # Skip drawing the piece at the drag origin
                    if (
                        self._drag_state.is_dragging
                        and self._drag_state.origin
                        and self._drag_state.origin.row == row
                        and self._drag_state.origin.col == col
                    ):
                        continue
                    piece_surf = self._piece_surfaces[(piece.piece_type, piece.color)]
                    x = self._board_x + col * sq
                    y = self._board_y + row * sq
                    self.surface.blit(piece_surf, (x, y))

        # Draw dragged piece at cursor
        if (
            self._drag_state.is_dragging
            and self._drag_state.piece
            and self._drag_state.mouse_pos
        ):
            piece = self._drag_state.piece
            piece_surf = self._piece_surfaces[(piece.piece_type, piece.color)]
            mx, my = self._drag_state.mouse_pos
            self.surface.blit(piece_surf, (mx - sq // 2, my - sq // 2))

        # Turn indicator / status text
        self._draw_status()

        # Back button
        self._back_button.draw(self.surface)

    def _draw_highlights(self) -> None:
        """Draw highlights on the origin square and legal move destinations."""
        sq = self._square_size

        # Highlight origin square with blue tint
        if self._drag_state.origin:
            origin_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)
            origin_surf.fill(COLOR_HIGHLIGHT_ORIGIN)
            ox = self._board_x + self._drag_state.origin.col * sq
            oy = self._board_y + self._drag_state.origin.row * sq
            self.surface.blit(origin_surf, (ox, oy))

        # Draw legal move indicators
        board = self._game_controller.game_state.board
        for move_pos in self._drag_state.legal_moves:
            cx = self._board_x + move_pos.col * sq + sq // 2
            cy = self._board_y + move_pos.row * sq + sq // 2

            target = board.get_piece(move_pos)
            if target is not None:
                # Capture highlight: semi-transparent ring
                ring_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)
                pygame.draw.circle(
                    ring_surf, (0, 0, 0, 60), (sq // 2, sq // 2), sq // 2 - 2, 4
                )
                self.surface.blit(
                    ring_surf,
                    (
                        self._board_x + move_pos.col * sq,
                        self._board_y + move_pos.row * sq,
                    ),
                )
            else:
                # Normal move: small dot
                dot_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)
                pygame.draw.circle(dot_surf, (0, 0, 0, 60), (sq // 2, sq // 2), sq // 6)
                self.surface.blit(
                    dot_surf,
                    (
                        self._board_x + move_pos.col * sq,
                        self._board_y + move_pos.row * sq,
                    ),
                )

    def _draw_status(self) -> None:
        """Draw turn indicator and game status text."""
        game_state = self._game_controller.game_state
        if game_state.is_game_over():
            text = game_state.get_result_message()
        elif game_state.status == GameStatus.CHECK:
            turn_name = game_state.board.current_turn.name.capitalize()
            text = f"{turn_name}'s turn - CHECK!"
        else:
            turn_name = game_state.board.current_turn.name.capitalize()
            text = f"{turn_name}'s turn"

        status_surf = self._status_font.render(text, True, COLOR_TEXT)
        status_rect = status_surf.get_rect(
            centerx=self.surface.get_width() // 2, top=20
        )
        self.surface.blit(status_surf, status_rect)
