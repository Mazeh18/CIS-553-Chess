from typing import Optional


class TimeControl:
    """Represents a time control configuration for a game."""

    def __init__(
        self,
        name: str,
        time_minutes: Optional[int],
        increment_seconds: int,
    ) -> None:
        self.name = name
        self.time_minutes = time_minutes
        self.increment_seconds = increment_seconds

    def is_timed(self) -> bool:
        """Return True if a time limit is active."""
        return self.time_minutes is not None

    def get_starting_seconds(self) -> float:
        """Convert time_minutes to seconds. Returns 0.0 if untimed."""
        if self.time_minutes is None:
            return 0.0
        return float(self.time_minutes * 60)
