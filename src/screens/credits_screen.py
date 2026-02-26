from typing import Callable, Optional

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.constants import (
    COLOR_BACKGROUND,
    COLOR_TEXT,
    FONT_NAME,
    FONT_SIZE_HEADING,
    FONT_SIZE_BODY,
    FONT_SIZE_BUTTON,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

AUTHORS = [
    "Ahmad Mazeh",
    "Austin Vetor",
    "Eya Mallat",
    "Garima Singh",
    "Nick Presley",
    "Nicole Kuang",
]


class CreditsScreen(BaseScreen):
    """Credits screen showing author names with a Back button."""

    def __init__(
        self,
        surface: pygame.Surface,
        on_back: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(surface)

        screen_w, screen_h = surface.get_size()
        center_x = screen_w // 2

        heading_font = pygame.font.Font(FONT_NAME, FONT_SIZE_HEADING)
        subheading_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BUTTON)
        body_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)

        # Title
        self._title_surface = heading_font.render("Credits", True, COLOR_TEXT)
        self._title_rect = self._title_surface.get_rect(
            centerx=center_x, centery=screen_h // 6
        )

        # "Developed By:" subheading
        self._dev_surface = subheading_font.render("Developed By:", True, COLOR_TEXT)
        self._dev_rect = self._dev_surface.get_rect(
            centerx=center_x, centery=screen_h // 6 + 80
        )

        # Author names
        self._author_surfaces = []
        line_height = 36
        start_y = screen_h // 6 + 130
        for i, name in enumerate(AUTHORS):
            surf = body_font.render(name, True, COLOR_TEXT)
            rect = surf.get_rect(centerx=center_x, centery=start_y + i * line_height)
            self._author_surfaces.append((surf, rect))

        # Back button near bottom
        self._back_button = Button(
            label="Back",
            rect=pygame.Rect(
                center_x - BUTTON_WIDTH // 2,
                screen_h - 120,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
            on_click=on_back,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        self._back_button.handle_event(event)

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.surface.fill(COLOR_BACKGROUND)
        self.surface.blit(self._title_surface, self._title_rect)
        self.surface.blit(self._dev_surface, self._dev_rect)
        for surf, rect in self._author_surfaces:
            self.surface.blit(surf, rect)
        self._back_button.draw(self.surface)
