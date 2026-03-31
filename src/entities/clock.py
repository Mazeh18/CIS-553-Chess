from typing import Optional
from src.entities.enums import Color

class Clock:
    """Manages both players' chess clocks"""

    def __init__(self):
        self.white_time: float = 0
        self.black_time: float = 0
        self.increment: int = 0
        self.is_running: bool = False
        self.active_color: Optional[Color] = None
        self.enabled: bool = False

    def get_time(self, color: Color) -> float:
        pass

    def tick(self, delta: float) -> None:
        """Decrements active player's time"""
        pass

    def add_increment(self, color: Color) -> None:
        """Adds time increment after a move"""
        pass

    def start(self, color: Color) -> None:
        pass

    def stop(self) -> None:
        pass

    def is_time_expired(self, color: Color) -> bool:
        pass

    def format_time(self, color: Color) -> str:
        """Return a formatted display string"""
        pass
