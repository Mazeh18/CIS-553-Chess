from abc import ABC, abstractmethod

from src.constants import (
    BASE_HEIGHT,
    BASE_WIDTH
)

import pygame


class BaseScreen(ABC):
    """Abstract base class for all application screens."""

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    def create_virtual_event(self, event: pygame.event.Event) -> pygame.event.Event:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            # Scale Mouse input to virtual screen:
            sw,sh = self.surface.get_size()
            scale = min(sw / BASE_WIDTH, sh / BASE_HEIGHT)
            offset_x = (sw - int(BASE_WIDTH * scale)) // 2
            offset_y = (sh - int(BASE_HEIGHT * scale)) // 2
            x, y = event.pos
            virtual_x = (x - offset_x) / scale
            virtual_y = (y - offset_y) / scale
            virtual_event = pygame.event.Event(
                event.type,
                pos=(virtual_x, virtual_y),
                button=getattr(event,"button",None),
                rel=getattr(event, "rel", (0,0)),
                buttons=getattr(event, "buttons", (0,0,0))
            )
            return virtual_event
        else:
            return event