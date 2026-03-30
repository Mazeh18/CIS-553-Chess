from typing import Callable, Optional

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.constants import (
    COLOR_BACKGROUND,
    COLOR_TEXT,
    FONT_NAME,
    FONT_SIZE_TITLE,
    FONT_SIZE_HEADING,
    FONT_SIZE_BODY,
    FONT_SIZE_BUTTON,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BASE_HEIGHT,
    BASE_WIDTH
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

        self._virtual_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        screen_w, screen_h = self._virtual_surface.get_size()
        center_x = screen_w // 2

        heading_font = pygame.font.Font(FONT_NAME, FONT_SIZE_TITLE)
        subheading_font = pygame.font.Font(FONT_NAME, FONT_SIZE_HEADING)
        body_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)
        
        # Background
        self._scaled_back = pygame.transform.scale(COLOR_BACKGROUND.convert_alpha(), self.surface.get_size())
        
        # Queen Decals
        self._decal_white_pos = (center_x - 700, screen_h // 2 - 200)
        self._decal_black_pos = (center_x + 400, screen_h // 2 - 200)
        self._wq_decal = pygame.transform.scale(pygame.image.load("assets/MenuPieces/QWhiteDecal.png").convert_alpha(), (300, screen_h//2))
        self._bq_decal = pygame.transform.scale(pygame.image.load("assets/MenuPieces/QBlackDecal.png").convert_alpha(), (300, screen_h//2))

        # Title
        self._title_surface = heading_font.render("Credits", True, COLOR_TEXT)
        self._title_rect = self._title_surface.get_rect(
            centerx=center_x, centery=screen_h // 6
        )

        # "Developed By:" subheading
        self._dev_surface = subheading_font.render("Developed By:", True, COLOR_TEXT)
        self._dev_rect = self._dev_surface.get_rect(
            centerx=center_x, centery=screen_h // 6 + 120
        )

        # Author names
        self._author_surfaces = []
        line_height = 64
        start_y = screen_h // 6 + 240
        for i, name in enumerate(AUTHORS):
            surf = body_font.render(name, True, COLOR_TEXT)
            rect = surf.get_rect(centerx=center_x, centery=start_y + i * line_height)
            self._author_surfaces.append((surf, rect))

        # Back button near bottom
        self._back_button = Button(
            label="Back",
            rect=pygame.Rect(
                center_x - (BUTTON_WIDTH+60) // 2,
                screen_h - 200,
                BUTTON_WIDTH+60,
                BUTTON_HEIGHT+30,
            ),
            on_click=on_back,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        sw,sh = self.surface.get_size()
        scale = min(sw / BASE_WIDTH, sh / BASE_HEIGHT)
        offset_x = (sw - int(BASE_WIDTH * scale))
        offset_y = (sh - int(BASE_HEIGHT * scale))
        x, y = event.pos
        virtual_x = (x - offset_x) / scale
        virtual_y = (y - offset_y) / scale
        event.pos = (virtual_x, virtual_y)
        self._back_button.handle_event(event)

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self._virtual_surface.blit(self._scaled_back, (0,0))
        self._virtual_surface.blit(self._wq_decal, self._decal_white_pos)
        self._virtual_surface.blit(self._bq_decal, self._decal_black_pos)
        self._virtual_surface.blit(self._title_surface, self._title_rect)
        self._virtual_surface.blit(self._dev_surface, self._dev_rect)
        for surf, rect in self._author_surfaces:
            self._virtual_surface.blit(surf, rect)
        self._back_button.draw(self._virtual_surface)

        scaled_virtual = pygame.transform.smoothscale(self._virtual_surface, self.surface.get_size())
        self.surface.blit(scaled_virtual, (0,0))