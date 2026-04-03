from typing import Optional
from src.entities.clock import Clock
from src.entities.time_control import TimeControl
from src.entities.enums import Color

class ClockController:
    """Manages clock countdown and timeout detection"""

    def __init__(self):
        self.clock: Optional[Clock] = None

    def initialize(self, time_control: TimeControl):
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
        self.clock.tick(delta)
        if self.clock.is_time_expired(self.clock.active_color):
            return True
        else:
            return False

    def switch_turn(self, color: Color):
        self.clock.add_increment(color)
        self.clock.stop()
        self.clock.start(color.opposite())
