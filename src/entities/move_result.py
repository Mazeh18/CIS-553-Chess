from src.entities.enums import GameStatus


class MoveResult:
    """Result of a move attempt, returned by GameController."""

    def __init__(
        self, success: bool, is_promotion: bool, new_status: GameStatus
    ) -> None:
        self.success = success
        self.is_promotion = is_promotion
        self.new_status = new_status
