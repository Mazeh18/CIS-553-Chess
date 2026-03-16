from typing import Callable, Optional, Tuple

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.components.text_input import TextInput
from src.constants import (
    COLOR_BACKGROUND,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    FONT_NAME,
    FONT_SIZE_HEADING,
    FONT_SIZE_BODY,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_SPACING,
)

# (label, minutes or None, increment_seconds)
PRESETS = [
    ("Bullet\n(2+1)", 2, 1),
    ("Blitz\n(5+0)", 5, 0),
    ("Rapid\n(10+5)", 10, 5),
    ("Classic\n(30+20)", 30, 20),
    ("No Time", None, 0),
    ("Custom", None, None),  # sentinel — triggers custom view
]


class TimeSelectScreen(BaseScreen):
    """Time control selection with presets and custom entry."""

    def __init__(
        self,
        surface: pygame.Surface,
        on_time_selected: Optional[Callable[[Optional[int], int], None]] = None,
        on_back: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(surface)

        self._on_time_selected = on_time_selected
        self._on_back = on_back
        self._showing_custom = False

        screen_w, screen_h = surface.get_size()
        center_x = screen_w // 2

        heading_font = pygame.font.Font(FONT_NAME, FONT_SIZE_HEADING)
        
        # Background
        self._scaled_back = pygame.transform.scale(COLOR_BACKGROUND.convert_alpha(), self.surface.get_size())
        
        # ── Preset view ───────────────────────────────────────
        self._preset_title_surface = heading_font.render(
            "Select Time Control", True, COLOR_TEXT
        )
        self._preset_title_rect = self._preset_title_surface.get_rect(
            centerx=center_x, centery=screen_h // 6
        )

        # 2x3 grid of preset buttons
        btn_w, btn_h = BUTTON_WIDTH + 100, BUTTON_HEIGHT + 100
        grid_gap = BUTTON_SPACING + 20
        cols, rows = 3, 2
        grid_w = cols * btn_w + (cols - 1) * grid_gap
        grid_h = rows * btn_h + (rows - 1) * grid_gap
        grid_x = center_x - grid_w // 2
        grid_y = screen_h // 3 - grid_h // 2 + 100

        self._preset_buttons: list[Button] = []
        for i, (label, minutes, increment) in enumerate(PRESETS):
            col = i % cols
            row = i // cols
            x = grid_x + col * (btn_w + grid_gap)
            y = grid_y + row * (btn_h + grid_gap)

            if label.startswith("Custom"):
                cb = self._show_custom
            else:
                cb = self._make_preset_callback(minutes, increment)

            self._preset_buttons.append(
                Button(label=label, rect=pygame.Rect(x, y, btn_w, btn_h), on_click=cb)
            )

        # Back button
        self._preset_back = Button(
            label="Back",
            rect=pygame.Rect(
                center_x - (BUTTON_WIDTH + 40) // 2,
                grid_y + grid_h + 60,
                BUTTON_WIDTH + 40,
                BUTTON_HEIGHT + 40,
            ),
            on_click=on_back,
        )

        # ── Custom view ───────────────────────────────────────
        self._custom_title_surface = heading_font.render(
            "Custom Time Control", True, COLOR_TEXT
        )
        self._custom_title_rect = self._custom_title_surface.get_rect(
            centerx=center_x, centery=screen_h // 6
        )

        input_w, input_h = 120, 44
        input_y = screen_h // 3 + 10
        gap = 60

        self._minutes_input = TextInput(
            label="Minutes",
            rect=pygame.Rect(center_x - input_w - gap // 2, input_y, input_w, input_h),
        )
        self._increment_input = TextInput(
            label="Increment (sec)",
            rect=pygame.Rect(center_x + gap // 2, input_y, input_w, input_h),
        )

        custom_btn_y = input_y + input_h + 50
        self._custom_start = Button(
            label="Start",
            rect=pygame.Rect(center_x - btn_w // 2, custom_btn_y, btn_w, btn_h),
            on_click=self._handle_custom_start,
        )
        self._custom_back = Button(
            label="Back",
            rect=pygame.Rect(
                center_x - btn_w // 2,
                custom_btn_y + btn_h + BUTTON_SPACING,
                btn_w,
                btn_h,
            ),
            on_click=self._hide_custom,
        )

        # Error text
        self._error_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)
        self._error_text: Optional[str] = None
        self._error_y = custom_btn_y - 30

    # ── Callbacks ──────────────────────────────────────────────

    def _make_preset_callback(
        self, minutes: Optional[int], increment: int
    ) -> Callable[[], None]:
        def cb():
            if self._on_time_selected:
                self._on_time_selected(minutes, increment)

        return cb

    def _show_custom(self) -> None:
        self._showing_custom = True
        self._error_text = None

    def _hide_custom(self) -> None:
        self._showing_custom = False
        self._minutes_input.value = ""
        self._increment_input.value = ""
        self._error_text = None

    def _handle_custom_start(self) -> None:
        minutes = self._minutes_input.get_int()
        increment = self._increment_input.get_int()

        if minutes is None or minutes <= 0:
            self._error_text = "Enter a valid number of minutes."
            return

        if increment is None:
            increment = 0

        self._error_text = None
        if self._on_time_selected:
            self._on_time_selected(minutes, increment)

    # ── Screen interface ──────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._showing_custom:
            self._minutes_input.handle_event(event)
            self._increment_input.handle_event(event)
            self._custom_start.handle_event(event)
            self._custom_back.handle_event(event)
        else:
            for btn in self._preset_buttons:
                btn.handle_event(event)
            self._preset_back.handle_event(event)

    def update(self, dt: float) -> None:
        if self._showing_custom:
            self._minutes_input.update(dt)
            self._increment_input.update(dt)

    def draw(self) -> None:
        self.surface.blit(self._scaled_back, (0,0))

        if self._showing_custom:
            self.surface.blit(self._custom_title_surface, self._custom_title_rect)
            self._minutes_input.draw(self.surface)
            self._increment_input.draw(self.surface)
            self._custom_start.draw(self.surface)
            self._custom_back.draw(self.surface)

            if self._error_text:
                err_surf = self._error_font.render(
                    self._error_text, True, (230, 80, 80)
                )
                err_rect = err_surf.get_rect(
                    centerx=self.surface.get_width() // 2, centery=self._error_y
                )
                self.surface.blit(err_surf, err_rect)
        else:
            self.surface.blit(self._preset_title_surface, self._preset_title_rect)
            for btn in self._preset_buttons:
                btn.draw(self.surface)
            self._preset_back.draw(self.surface)
