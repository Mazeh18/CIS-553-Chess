from abc import ABC, abstractmethod

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
