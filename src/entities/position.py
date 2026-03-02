class Position:
    """Represents a square on the board (row 0-7, col 0-7)."""

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def to_algebraic(self) -> str:
        """Convert to algebraic notation (e.g., 'e4')."""
        file = chr(ord('a') + self.col)
        rank = str(8 - self.row)
        return f"{file}{rank}"

    @staticmethod
    def from_algebraic(notation: str) -> "Position":
        """Create Position from algebraic notation (e.g., 'e4')."""
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return Position(row, col)

    def is_valid(self) -> bool:
        """Return True if row and col are within 0-7."""
        return 0 <= self.row <= 7 and 0 <= self.col <= 7

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self) -> str:
        return f"Position({self.row}, {self.col})"
