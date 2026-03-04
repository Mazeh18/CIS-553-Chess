import sys
from typing import Optional

import pygame

from src.entities.enums import ScreenType
from src.screens.base_screen import BaseScreen
from src.screens.start_menu_screen import StartMenuScreen
from src.screens.credits_screen import CreditsScreen
from src.screens.time_select_screen import TimeSelectScreen
from src.screens.game_screen import GameScreen


class ScreenNavigationController:
    """Manages screen transitions following the dialog map."""

    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface
        self.current_screen_type: ScreenType = ScreenType.START_MENU
        self.current_screen: Optional[BaseScreen] = None
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

    def navigate_to_game(self) -> None:
        self.current_screen_type = ScreenType.GAME
        self.current_screen = GameScreen(
            surface=self._surface,
            on_back=self.navigate_to_start_menu,
        )

    def handle_exit(self) -> None:
        pygame.quit()
        sys.exit()

    def _handle_time_selected(
        self, minutes: Optional[int], increment: int
    ) -> None:
        # Time control values are available here for future use.
        # For now, just navigate to the game screen.
        self.navigate_to_game()
