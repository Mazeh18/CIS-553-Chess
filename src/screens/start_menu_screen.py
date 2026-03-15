from typing import Callable, Optional

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.constants import (
    COLOR_BACKGROUND,
    COLOR_TEXT,
    FONT_NAME,
    FONT_SIZE_TITLE,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_SPACING,
)


class StartMenuScreen(BaseScreen):
    """Start menu with Play, Credits, and Exit buttons."""

    def __init__(
        self,
        surface: pygame.Surface,
        on_play: Optional[Callable[[], None]] = None,
        on_credits: Optional[Callable[[], None]] = None,
        on_exit: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(surface)

        self._title_font = pygame.font.Font(FONT_NAME, FONT_SIZE_TITLE)

        screen_w, screen_h = surface.get_size()
        center_x = screen_w // 2

        # Title in upper quarter
        self._title_surface = self._title_font.render("CHESS", True, COLOR_TEXT)
        self._title_rect = self._title_surface.get_rect(
            centerx=center_x, centery=screen_h // 4
        )

        # Buttons centered vertically below midpoint
        button_start_y = screen_h // 2 - 30
        button_x = center_x - BUTTON_WIDTH // 2

        self._buttons = [
            Button(
                label="Play",
                rect=pygame.Rect(button_x, button_start_y, BUTTON_WIDTH, BUTTON_HEIGHT),
                on_click=on_play,
            ),
            Button(
                label="Credits",
                rect=pygame.Rect(
                    button_x,
                    button_start_y + BUTTON_HEIGHT + BUTTON_SPACING,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT,
                ),
                on_click=on_credits,
            ),
            Button(
                label="Exit",
                rect=pygame.Rect(
                    button_x,
                    button_start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING),
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT,
                ),
                on_click=on_exit,
            ),
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        for button in self._buttons:
            button.handle_event(event)

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.surface.fill(COLOR_BACKGROUND)
        self.surface.blit(self._title_surface, self._title_rect)
        for button in self._buttons:
            button.draw(self.surface)
