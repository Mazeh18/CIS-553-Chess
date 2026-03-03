from typing import Callable, Optional

import pygame

from src.constants import (
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_BUTTON_DISABLED,
    COLOR_BUTTON_TEXT,
    COLOR_TEXT_DIM,
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

        scaled_image = pygame.transform.scale(bg_color, self.rect.size)
        surface.blit(scaled_image, self.rect)
<<<<<<< HEAD
        
        # Text wrapping
        lines = self.label.split("\n")
        line_height = self._font.get_height()
        total_height = len(lines) * line_height
        y_offset = self.rect.y + (self.rect.height - total_height) // 2
        for line in lines:
            text_surface = self._font.render(line.strip(), True, text_color)
            text_rect = text_surface.get_rect(centerx=self.rect.centerx)
            text_rect.y = y_offset
            surface.blit(text_surface, text_rect)
            y_offset += line_height
            
        
=======

        text_surface = self._font.render(self.label, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
>>>>>>> 656e914 (Added button asset and began customizing it to the menus.)
