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
        if color == Color.WHITE:
            return self.white_time
        else:
            return self.black_time

    def tick(self, delta: float) -> None:
        """Decrements active player's time"""
        if self.active_color == Color.WHITE:
            self.white_time -= delta
        else:
            self.black_time -= delta

    def add_increment(self, color: Color) -> None:
        """Adds time increment after a move"""
        if color == Color.WHITE:
            self.white_time += self.increment
        else:
            self.black_time += self.increment

    def start(self, color: Color) -> None:
        self.active_color = color
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def is_time_expired(self, color: Color) -> bool:
        if color == Color.WHITE:
            return self.white_time == 0
        else:
            return self.black_time == 0

    def format_time(self, color: Color) -> str:
        """Return a formatted display string"""
        if color == Color.WHITE:
            minutes = int(self.white_time // 60)
            seconds = int(self.white_time % 60)
        else:
            minutes = int(self.black_time // 60)
            seconds = int(self.black_time % 60)

        if minutes <= 9:
            str_min = f"0{minutes}"
        else:
            str_min = str(minutes)

        if seconds <= 9:
            str_sec = f"0{seconds}"
        else:
            str_sec = str(seconds)

        return f"{str_min}:{str_sec}"
