import sys
from typing import Optional

import pygame

from src.entities.enums import ScreenType
from src.entities.time_control import TimeControl
from src.screens.base_screen import BaseScreen
from src.screens.start_menu_screen import StartMenuScreen
from src.screens.credits_screen import CreditsScreen
from src.screens.time_select_screen import TimeSelectScreen
from src.screens.game_screen import GameScreen
from src.controllers.game_controller import GameController


class ScreenNavigationController:
    """Manages screen transitions following the dialog map."""

    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface
        self.current_screen_type: ScreenType = ScreenType.START_MENU
        self.current_screen: Optional[BaseScreen] = None
        self._game_controller = GameController()
        self.navigate_to_start_menu()

    def navigate_to_start_menu(self) -> None:
        self.current_screen_type = ScreenType.START_MENU
        self.current_screen = StartMenuScreen(
            surface=self._surface,
            on_play=self.navigate_to_time_select,
            on_credits=self.navigate_to_credits,
            on_exit=self.handle_exit,
        )

    def navigate_to_credits(self) -> None:
        self.current_screen_type = ScreenType.CREDITS
        self.current_screen = CreditsScreen(
            surface=self._surface,
            on_back=self.navigate_to_start_menu,
        )

    def navigate_to_time_select(self) -> None:
        self.current_screen_type = ScreenType.TIME_SELECT
        self.current_screen = TimeSelectScreen(
            surface=self._surface,
            on_time_selected=self._handle_time_selected,
            on_back=self.navigate_to_start_menu,
        )

    def navigate_to_game(self, time_control: TimeControl) -> None:
        self._game_controller.new_game(time_control)
        self.current_screen_type = ScreenType.GAME
        self.current_screen = GameScreen(
            surface=self._surface,
            game_controller=self._game_controller,
            on_back=self.navigate_to_start_menu,
            on_new=self.navigate_to_time_select,
        )

    def handle_exit(self) -> None:
        pygame.quit()
        sys.exit()

    def _handle_time_selected(self, minutes: Optional[int], increment: int) -> None:
        if minutes is None:
            name = "No Time"
        else:
            name = f"{minutes}+{increment}"
        tc = TimeControl(name=name, time_minutes=minutes, increment_seconds=increment)
        self.navigate_to_game(tc)
