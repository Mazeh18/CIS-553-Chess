from src.entities.time_control import TimeControl
from src.entities.enums import Color

class ClockController:
    """Manages clock countdown and timeout detection"""

    def initialize(self, time_control: TimeControl):
        pass

    def start_clock(self, color: Color):
        pass

    def stop_clock(self):
        pass

    def update(self, delta: float) -> bool:
        pass

    def switch_turn(self, color: Color):
        pass
