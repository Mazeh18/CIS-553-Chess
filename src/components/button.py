from typing import Callable, Optional

import pygame

from src.constants import (
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_BUTTON_DISABLED,
    COLOR_BUTTON_TEXT,
    COLOR_TEXT_DIM,
    COLOR_BUTTON_BORDER,
    BUTTON_BORDER_RADIUS,
    FONT_NAME,
    FONT_SIZE_BUTTON,
)


class Button:
    """Reusable clickable button with hover and disabled states."""

    def __init__(
        self,
        label: str,
        rect: pygame.Rect,
        on_click: Optional[Callable[[], None]] = None,
        enabled: bool = True,
    ) -> None:
        self.label = label
        self.rect = rect
        self.on_click = on_click
        self.enabled = enabled
        self.hovered = False
        self._font = pygame.font.Font(FONT_NAME, FONT_SIZE_BUTTON)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled:
            self.hovered = False
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.on_click:
                self.on_click()

    def draw(self, surface: pygame.Surface) -> None:
        if not self.enabled:
            bg_color = COLOR_BUTTON_DISABLED
            text_color = COLOR_TEXT_DIM
        elif self.hovered:
            bg_color = COLOR_BUTTON_HOVER
            text_color = COLOR_BUTTON_TEXT
        else:
            bg_color = COLOR_BUTTON
            text_color = COLOR_BUTTON_TEXT

        pygame.draw.rect(
            surface, bg_color, self.rect, border_radius=BUTTON_BORDER_RADIUS
        )
        pygame.draw.rect(
            surface, COLOR_BUTTON_BORDER, self.rect,
            width=2, border_radius=BUTTON_BORDER_RADIUS,
        )

        text_surface = self._font.render(self.label, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
