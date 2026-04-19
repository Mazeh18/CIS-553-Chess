from typing import Optional
from src.entities.clock import Clock
from src.entities.time_control import TimeControl
from src.entities.enums import Color

class ClockController:
    """Manages clock countdown and timeout detection"""

    def __init__(self):
        self.clock: Optional[Clock] = None

    def initialize(self, time_control: TimeControl):
        """Sets starting minutes and enables clock if a time is selected"""
        if time_control.name != "No Time":
            self.clock.white_time = time_control.get_starting_seconds()
            self.clock.black_time = time_control.get_starting_seconds()
            self.clock.increment = time_control.increment_seconds
            self.clock.enabled = True

    def start_clock(self, color: Color):
        self.clock.start(color)

    def stop_clock(self):
        self.clock.stop()

    def update(self, delta: float) -> bool:
        """Ticks timer down, returns True if timer is up"""
        self.clock.tick(delta)
        if self.clock.is_time_expired(self.clock.active_color) and self.clock.enabled:
            return True
        else:
            return False

    def switch_turn(self, color: Color):
        """Adds increment after a move and switches turns"""
        self.clock.stop()
        self.clock.add_increment(color)
        self.clock.start(color.opposite())
