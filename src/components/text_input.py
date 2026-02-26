from typing import Optional

import pygame

from src.constants import (
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLOR_BUTTON_BORDER,
    COLOR_PANEL,
    FONT_NAME,
    FONT_SIZE_BODY,
)


class TextInput:
    """Numeric text input field with label and underline style."""

    def __init__(
        self,
        label: str,
        rect: pygame.Rect,
        max_digits: int = 3,
    ) -> None:
        self.label = label
        self.rect = rect
        self.value = ""
        self.focused = False
        self._max_digits = max_digits
        self._label_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)
        self._value_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)
        self._cursor_visible = True
        self._cursor_timer = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focused = self.rect.collidepoint(event.pos)

        if not self.focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.unicode.isdigit() and len(self.value) < self._max_digits:
                self.value += event.unicode

    def update(self, dt: float) -> None:
        self._cursor_timer += dt
        if self._cursor_timer >= 0.5:
            self._cursor_timer = 0.0
            self._cursor_visible = not self._cursor_visible

    def draw(self, surface: pygame.Surface) -> None:
        # Label above the input box
        label_surf = self._label_font.render(self.label, True, COLOR_TEXT_DIM)
        label_rect = label_surf.get_rect(
            centerx=self.rect.centerx, bottom=self.rect.top - 4
        )
        surface.blit(label_surf, label_rect)

        # Input background
        bg_color = COLOR_PANEL if not self.focused else (70, 68, 65)
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)

        # Border
        border_color = COLOR_TEXT if self.focused else COLOR_BUTTON_BORDER
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=6)

        # Value text
        display = self.value
        if self.focused and self._cursor_visible:
            display += "|"
        value_surf = self._value_font.render(display, True, COLOR_TEXT)
        value_rect = value_surf.get_rect(center=self.rect.center)
        surface.blit(value_surf, value_rect)

    def get_int(self) -> Optional[int]:
        """Return the value as int, or None if empty."""
        return int(self.value) if self.value else None
