from src.entities.position import Position


class MoveAttempt:
    """Input from InputController to GameController. Pairs start and end positions."""

    def __init__(self, start_pos: Position, end_pos: Position) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
