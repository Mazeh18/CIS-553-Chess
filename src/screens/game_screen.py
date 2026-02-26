from typing import Callable, Optional

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.entities.enums import Color, PieceType
from src.constants import (
    COLOR_BACKGROUND,
<<<<<<< HEAD
    LIGHT_SQUARE,
    DARK_SQUARE,
    BOARD_BORDER,
    BOARD_BORDER_P,
    COLOR_TEXT,
=======
    COLOR_LIGHT_SQUARE,
    COLOR_DARK_SQUARE,
    COLOR_TEXT,
    COLOR_LABEL,
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)
    FONT_NAME,
    FONT_SIZE_SMALL,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# ── Piece rendering ────────────────────────────────────────────────────
# Placeholder assets: colored circles with a letter abbreviation.
# To swap in real PNGs later, replace _draw_piece() or load images into
# PIECE_IMAGES and blit them instead.

<<<<<<< HEAD
PIECES = {
=======
PIECE_LETTER = {
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)
    PieceType.KING: "K",
    PieceType.QUEEN: "Q",
    PieceType.ROOK: "R",
    PieceType.BISHOP: "B",
    PieceType.KNIGHT: "N",
    PieceType.PAWN: "P",
}

<<<<<<< HEAD
PIECE_WHITE = {
    PieceType.PAWN: pygame.image.load("assets/Pieces/PawnWhite.png")
}

PIECE_BLACK = {
    PieceType.PAWN: pygame.image.load("assets/Pieces/PawnBlack.png")
}

=======
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)
COLOR_WHITE_PIECE = (255, 255, 255)
COLOR_BLACK_PIECE = (30, 30, 30)
COLOR_WHITE_PIECE_TEXT = (30, 30, 30)
COLOR_BLACK_PIECE_TEXT = (220, 220, 220)

# Standard starting position — (PieceType, Color) or None for each square.
# Board index: row 0 = rank 8 (Black back rank), row 7 = rank 1 (White back rank).
INITIAL_BOARD = [
    # rank 8
    [(PieceType.ROOK, Color.BLACK), (PieceType.KNIGHT, Color.BLACK),
     (PieceType.BISHOP, Color.BLACK), (PieceType.QUEEN, Color.BLACK),
     (PieceType.KING, Color.BLACK), (PieceType.BISHOP, Color.BLACK),
     (PieceType.KNIGHT, Color.BLACK), (PieceType.ROOK, Color.BLACK)],
    # rank 7
    [(PieceType.PAWN, Color.BLACK)] * 8,
    # ranks 6-3 (empty)
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    # rank 2
    [(PieceType.PAWN, Color.WHITE)] * 8,
    # rank 1
    [(PieceType.ROOK, Color.WHITE), (PieceType.KNIGHT, Color.WHITE),
     (PieceType.BISHOP, Color.WHITE), (PieceType.QUEEN, Color.WHITE),
     (PieceType.KING, Color.WHITE), (PieceType.BISHOP, Color.WHITE),
     (PieceType.KNIGHT, Color.WHITE), (PieceType.ROOK, Color.WHITE)],
]

FILE_LABELS = "abcdefgh"
RANK_LABELS = "87654321"


class GameScreen(BaseScreen):
    """Game screen showing the chessboard with pieces (visual only)."""

    def __init__(
        self,
        surface: pygame.Surface,
        on_back: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(surface)

        screen_w, screen_h = surface.get_size()

<<<<<<< HEAD
        # Board sizing: fit to ~60% of screen height, left centered
        board_margin = 300
        self._square_size = (screen_h - board_margin * 2) // 8
        self._board_size = self._square_size * 8
        self._border_size = self._board_size + (BOARD_BORDER_P * 2)
        
        # Background
        self._scaled_back = pygame.transform.scale(COLOR_BACKGROUND.convert_alpha(), self.surface.get_size())
        
        # Position board center-left
        self._board_x = 100
=======
        # Board sizing: fit to ~85% of screen height, centered vertically
        board_margin = 40
        self._square_size = (screen_h - board_margin * 2) // 8
        self._board_size = self._square_size * 8

        # Position board center-left
        self._board_x = (screen_w - self._board_size) // 2
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)
        self._board_y = (screen_h - self._board_size) // 2

        # Fonts
        self._label_font = pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL)
        self._piece_font = pygame.font.Font(
            FONT_NAME, int(self._square_size * 0.45)
        )

        # Back button (top-left corner)
        self._back_button = Button(
            label="Back to Menu",
            rect=pygame.Rect(20, 20, BUTTON_WIDTH, BUTTON_HEIGHT),
            on_click=on_back,
        )

        # Pre-render the board surface (squares + labels) since it's static
        self._board_surface = self._render_board()

        # Pre-render piece surfaces keyed by (PieceType, Color)
        self._piece_surfaces = self._render_pieces()

    def _render_board(self) -> pygame.Surface:
        """Draw the 8x8 board with rank/file labels onto a surface."""
        sq = self._square_size
<<<<<<< HEAD
        playable_surf = pygame.Surface((self._board_size, self._board_size))
        border_surf = pygame.Surface((self._border_size, self._border_size))
        border = pygame.transform.scale(BOARD_BORDER.convert_alpha(), (self._border_size, self._border_size))
        border_surf.blit(border, (0, 0))
        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE.convert_alpha() if is_light else DARK_SQUARE.convert_alpha()
                playable_surf.blit(color, (col * sq,row * sq, sq, sq))

        border_surf.blit(playable_surf, (BOARD_BORDER_P,BOARD_BORDER_P))
        return border_surf
=======
        surf = pygame.Surface((self._board_size, self._board_size))

        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = COLOR_LIGHT_SQUARE if is_light else COLOR_DARK_SQUARE
                pygame.draw.rect(surf, color, (col * sq, row * sq, sq, sq))

        # File labels (a-h) along the bottom
        for col in range(8):
            label = self._label_font.render(FILE_LABELS[col], True, COLOR_LABEL)
            surf.blit(label, (col * sq + sq - label.get_width() - 2,
                              7 * sq + sq - label.get_height() - 1))

        # Rank labels (8-1) along the left
        for row in range(8):
            label = self._label_font.render(RANK_LABELS[row], True, COLOR_LABEL)
            surf.blit(label, (2, row * sq + 1))

        return surf
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)

    def _render_pieces(self) -> dict:
        """Pre-render placeholder piece surfaces (circle + letter)."""
        sq = self._square_size
        radius = int(sq * 0.38)
        surfaces = {}
<<<<<<< HEAD
        for piece_type in PieceType:
            for color in Color:
                if piece_type == PieceType.PAWN:
                    piece = (
                        pygame.transform.scale(PIECE_WHITE[PieceType.PAWN].convert_alpha(), (sq,sq))
                        if color == Color.WHITE
                        else pygame.transform.scale(PIECE_BLACK[PieceType.PAWN].convert_alpha(), (sq,sq))
                    )
                    piece_surf = pygame.Surface((sq,sq), pygame.SRCALPHA)
                    piece_surf.blit(piece, piece_surf.get_rect(center=(sq // 2, sq // 2)))
                else:
                    piece_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)

                    # Circle
                    circle_color = (
                        COLOR_WHITE_PIECE if color == Color.WHITE else COLOR_BLACK_PIECE
                    )
                    pygame.draw.circle(
                        piece_surf, circle_color, (sq // 2, sq // 2), radius
                    )
                    # Border on circle for contrast
                    border_color = (
                        (180, 180, 180) if color == Color.WHITE else (80, 80, 80)
                    )
                    pygame.draw.circle(
                        piece_surf, border_color, (sq // 2, sq // 2), radius, 2
                    )

                    # Letter
                    text_color = (
                        COLOR_WHITE_PIECE_TEXT
                        if color == Color.WHITE
                        else COLOR_BLACK_PIECE_TEXT
                    )
                    letter_surf = self._piece_font.render(
                        PIECES[piece_type], True, text_color
                    )
                    letter_rect = letter_surf.get_rect(center=(sq // 2, sq // 2))
                    piece_surf.blit(letter_surf, letter_rect)
=======

        for piece_type in PieceType:
            for color in Color:
                piece_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)

                # Circle
                circle_color = (
                    COLOR_WHITE_PIECE if color == Color.WHITE else COLOR_BLACK_PIECE
                )
                pygame.draw.circle(
                    piece_surf, circle_color, (sq // 2, sq // 2), radius
                )
                # Border on circle for contrast
                border_color = (
                    (180, 180, 180) if color == Color.WHITE else (80, 80, 80)
                )
                pygame.draw.circle(
                    piece_surf, border_color, (sq // 2, sq // 2), radius, 2
                )

                # Letter
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
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)

                surfaces[(piece_type, color)] = piece_surf

        return surfaces

    def handle_event(self, event: pygame.event.Event) -> None:
        self._back_button.handle_event(event)

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
<<<<<<< HEAD
        self.surface.blit(self._scaled_back, (0,0))
=======
        self.surface.fill(COLOR_BACKGROUND)
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)

        # Board
        self.surface.blit(self._board_surface, (self._board_x, self._board_y))

        # Pieces
        sq = self._square_size
        for row in range(8):
            for col in range(8):
                cell = INITIAL_BOARD[row][col]
                if cell is not None:
                    piece_type, color = cell
                    piece_surf = self._piece_surfaces[(piece_type, color)]
<<<<<<< HEAD
                    x = self._board_x + col * sq + BOARD_BORDER_P
                    y = self._board_y + row * sq + BOARD_BORDER_P
=======
                    x = self._board_x + col * sq
                    y = self._board_y + row * sq
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)
                    self.surface.blit(piece_surf, (x, y))

        # Back button
        self._back_button.draw(self.surface)
<<<<<<< HEAD

=======
>>>>>>> 722e78f (Add base application scaffold with main menu, credits, time control, and board screens)
