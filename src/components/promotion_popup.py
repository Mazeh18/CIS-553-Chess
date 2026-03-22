from typing import Callable, Optional

import pygame

from src.entities.enums import Color, PieceType
from src.entities.position import Position
from src.constants import COLOR_PANEL, COLOR_TEXT, COLOR_BUTTON_HOVER

# Promotion options in display order
PROMOTION_CHOICES = [
    PieceType.QUEEN,
    PieceType.ROOK,
    PieceType.BISHOP,
    PieceType.KNIGHT,
]

PIECE_LETTER = {
    PieceType.QUEEN: "Q",
    PieceType.ROOK: "R",
    PieceType.BISHOP: "B",
    PieceType.KNIGHT: "N",
}


class PromotionPopup:
    """Modal overlay showing 4 promotion piece options at the promotion column."""

    def __init__(
        self,
        surface: pygame.Surface,
        square_size: int,
        board_x: int,
        board_y: int,
        color: Color,
        position: Position,
        on_select: Callable[[PieceType], None],
    ) -> None:
        self._surface = surface
        self._square_size = square_size
        self._board_x = board_x
        self._board_y = board_y
        self._color = color
        self._position = position
        self._on_select = on_select

        # Build rects for the 4 options
        self._option_rects: list[tuple[pygame.Rect, PieceType]] = []
        col_px = board_x + position.col * square_size

        if color == Color.WHITE:
            # White promotes at row 0, extend downward (rows 0-3)
            start_row = 0
            direction = 1
        else:
            # Black promotes at row 7, extend upward (rows 7-4)
            start_row = 7
            direction = -1

        for i, piece_type in enumerate(PROMOTION_CHOICES):
            row = start_row + i * direction
            rect = pygame.Rect(
                col_px, board_y + row * square_size, square_size, square_size
            )
            self._option_rects.append((rect, piece_type))

        # Pre-render font
        self._font = pygame.font.Font(None, int(square_size * 0.5))

        # Piece rendering colors
        if color == Color.WHITE:
            self._circle_color = (255, 255, 255)
            self._text_color = (30, 30, 30)
            self._border_color = (180, 180, 180)
        else:
            self._circle_color = (30, 30, 30)
            self._text_color = (220, 220, 220)
            self._border_color = (80, 80, 80)

        self._hover_index: Optional[int] = None

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events. Returns True if the popup consumed the event."""
        if event.type == pygame.MOUSEMOTION:
            self._hover_index = None
            for i, (rect, _) in enumerate(self._option_rects):
                if rect.collidepoint(event.pos):
                    self._hover_index = i
                    break
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for _rect, piece_type in self._option_rects:
                if _rect.collidepoint(event.pos):
                    self._on_select(piece_type)
                    return True
            return True  # Block clicks outside options too (modal)

        if event.type == pygame.MOUSEBUTTONUP:
            return True

        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the promotion popup as a modal overlay."""
        sq = self._square_size
        radius = int(sq * 0.38)

        # Semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        for i, (rect, piece_type) in enumerate(self._option_rects):
            # Background
            bg_color = COLOR_BUTTON_HOVER if i == self._hover_index else COLOR_PANEL
            pygame.draw.rect(surface, bg_color, rect)
            pygame.draw.rect(surface, (200, 200, 200), rect, 2)

            # Piece circle
            cx, cy = rect.centerx, rect.centery
            pygame.draw.circle(surface, self._circle_color, (cx, cy), radius)
            pygame.draw.circle(surface, self._border_color, (cx, cy), radius, 2)

            # Piece letter
            letter_surf = self._font.render(
                PIECE_LETTER[piece_type], True, self._text_color
            )
            letter_rect = letter_surf.get_rect(center=(cx, cy))
            surface.blit(letter_surf, letter_rect)
