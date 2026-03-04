# Data Dictionary

This document defines the key data entities, attributes, and structures used in the chess application.

---

## 1. Application State

Top-level state tracking what screen the user is on.

| Attribute | Type | Description |
|-----------|------|-------------|
| current_screen | ScreenType (enum) | The screen currently displayed. Values: `START_MENU`, `CREDITS`, `TIME_SELECT`, `GAME`. |

---

## 2. Time Control

Represents the selected time control for a game.

| Attribute | Type | Description |
|-----------|------|-------------|
| name | str | Display name of the time control (e.g., "Bullet", "Blitz", "Custom"). |
| time_minutes | int or None | Starting time per player in minutes. `None` if no time control. |
| increment_seconds | int | Time added to a player's clock after each move, in seconds. 0 if no increment. |

### Derived Behavior

| Method | Returns | Description |
|--------|---------|-------------|
| `is_timed()` | bool | Returns `False` when `time_minutes` is `None` (i.e., "No Time" selected). |
| `get_starting_seconds()` | int | Returns `time_minutes * 60`. Returns 0 if not timed. |

### Preset Time Controls

| Name | time_minutes | increment_seconds |
|------|-------------|-------------------|
| Bullet | 2 | 1 |
| Blitz | 5 | 0 |
| Rapid (10+5) | 10 | 5 |
| Classic (30+20) | 30 | 20 |
| No Time | None | 0 |
| Custom | (user-defined) | (user-defined) |

---

## 3. Board

Represents the 8x8 game board.

| Attribute | Type | Description |
|-----------|------|-------------|
| squares | 2D array (8x8) of `Piece` or `None` | The grid representing the board. Indexed as `squares[row][col]` where row 0 is rank 8 (Black's back rank) and row 7 is rank 1 (White's back rank). |
| current_turn | Color (enum) | The player whose turn it is. Values: `WHITE`, `BLACK`. |
| move_history | list of `Move` | Ordered list of all moves made during the game. |
| halfmove_clock | int | Counter for the fifty-move rule. Incremented after each move; reset to 0 after a pawn move or capture. |
| fullmove_number | int | The current full move number. Starts at 1, increments after Black's move. |
| position_history | list of str | Board position hashes for threefold repetition detection. |

---

## 4. Piece

Represents a single chess piece.

| Attribute | Type | Description |
|-----------|------|-------------|
| piece_type | PieceType (enum) | The type of piece: `PAWN`, `ROOK`, `KNIGHT`, `BISHOP`, `QUEEN`, `KING`. |
| color | Color (enum) | The color of the piece: `WHITE`, `BLACK`. |
| has_moved | bool | Whether the piece has moved from its starting position. Used for castling rights and pawn double-move. |

### Standard Piece Values

| PieceType | Point Value |
|-----------|-------------|
| PAWN | 1 |
| KNIGHT | 3 |
| BISHOP | 3 |
| ROOK | 5 |
| QUEEN | 9 |
| KING | -- (not counted) |

---

## 5. Position

Represents a square on the board.

| Attribute | Type | Description |
|-----------|------|-------------|
| row | int | Row index (0-7). 0 = rank 8, 7 = rank 1. |
| col | int | Column index (0-7). 0 = file a, 7 = file h. |

---

## 6. Move

Represents a single move in the game.

| Attribute | Type | Description |
|-----------|------|-------------|
| piece | Piece | The piece being moved. |
| start_pos | Position | The starting square. |
| end_pos | Position | The destination square. |
| captured_piece | Piece or None | The piece captured by this move, if any. |
| is_castling | bool | Whether this move is a castling move. |
| is_en_passant | bool | Whether this move is an en passant capture. |
| promotion_piece | PieceType or None | The piece type chosen for pawn promotion, if applicable. |
| notation | str | The move in standard algebraic notation (e.g., "e4", "Nf3", "O-O"). |
| time_after_move | float or None | The moving player's remaining clock time after this move (for undo). `None` if no time control. |

---

## 7. Clock

Represents a player's chess clock.

| Attribute | Type | Description |
|-----------|------|-------------|
| white_time | float | White's remaining time in seconds. |
| black_time | float | Black's remaining time in seconds. |
| increment | int | Seconds added after each move. |
| is_running | bool | Whether the clock is currently counting down. |
| active_color | Color or None | Which player's clock is currently ticking. `None` if paused. |
| enabled | bool | Whether time controls are active for this game. `False` for "No Time" games. |

---

## 8. GameState

Represents the overall state of the game.

| Attribute | Type | Description |
|-----------|------|-------------|
| status | GameStatus (enum) | Current game status. |
| winner | Color or None | The winning player, or `None` if draw or still active. |
| board | Board | Reference to the Board object. |
| clock | Clock | Reference to the Clock object. |
| time_control | TimeControl | The time control selected for this game. |
| captured_pieces | CapturedPieces | Reference to the CapturedPieces object (see Section 10). Tracks all captured pieces and point advantage. |

---

## 9. Drag State

Tracks the state of a piece being dragged by the player.

| Attribute | Type | Description |
|-----------|------|-------------|
| is_dragging | bool | Whether a piece is currently being dragged. |
| piece | Piece or None | The piece being dragged. |
| origin | Position or None | The board square the piece was picked up from. |
| mouse_pos | tuple(int, int) | Current pixel position of the mouse cursor. Used to render the piece under the cursor. |
| legal_moves | list of Position | Legal destination squares for the dragged piece. Highlighted on the board. |

---

## 10. Captured Pieces / Point Advantage

| Attribute | Type | Description |
|-----------|------|-------------|
| white_captured | list of Piece | Pieces captured by White (Black's lost pieces). |
| black_captured | list of Piece | Pieces captured by Black (White's lost pieces). |
| white_points | int | Total point value of pieces White has captured. |
| black_points | int | Total point value of pieces Black has captured. |
| point_advantage | int | Difference: `white_points - black_points`. Positive = White leads, negative = Black leads. |

---

## 11. Enumerations

### ScreenType
| Value | Description |
|-------|-------------|
| START_MENU | The initial start menu screen. |
| CREDITS | The credits screen showing author information. |
| TIME_SELECT | The time control selection screen. |
| GAME | The main game screen. |

### Color
| Value | Description |
|-------|-------------|
| WHITE | White player / pieces. |
| BLACK | Black player / pieces. |

**Derived Behavior**: `opposite()` — Returns `BLACK` for `WHITE` and `WHITE` for `BLACK`.

### PieceType
| Value | Description |
|-------|-------------|
| PAWN | Pawn piece. |
| ROOK | Rook piece. |
| KNIGHT | Knight piece. |
| BISHOP | Bishop piece. |
| QUEEN | Queen piece. |
| KING | King piece. |

### GameStatus
| Value | Description |
|-------|-------------|
| ACTIVE | Game is in progress, no special state. |
| CHECK | Current player's King is in check. |
| CHECKMATE | Current player is in checkmate; game over. |
| STALEMATE | Current player has no legal moves; draw. |
| DRAW_INSUFFICIENT_MATERIAL | Not enough pieces to force checkmate; draw. |
| DRAW_THREEFOLD_REPETITION | Same position repeated three times; draw. |
| DRAW_FIFTY_MOVE | Fifty moves without pawn move or capture; draw. |
| RESIGNED | A player has resigned; game over. |
| TIMEOUT | A player's clock reached zero; game over. |

**Derived Behavior**:
- `is_game_over()` — Returns `True` for CHECKMATE, STALEMATE, DRAW_INSUFFICIENT_MATERIAL, DRAW_THREEFOLD_REPETITION, DRAW_FIFTY_MOVE, RESIGNED, TIMEOUT.
- `is_draw()` — Returns `True` for STALEMATE, DRAW_INSUFFICIENT_MATERIAL, DRAW_THREEFOLD_REPETITION, DRAW_FIFTY_MOVE.

---

## 12. Move History Entry (Display)

| Attribute | Type | Description |
|-----------|------|-------------|
| move_number | int | The full move number. |
| white_move | str | Algebraic notation for White's move (e.g., "e4", "Nf3", "O-O"). |
| black_move | str or None | Algebraic notation for Black's move, or `None` if White just moved. |

---

## 13. Move Result

A data transfer object returned by `GameController.attempt_move()` and `GameController.attempt_promotion()` to communicate the outcome of a move attempt back to the caller.

| Attribute | Type | Description |
|-----------|------|-------------|
| success | bool | Whether the move was successfully executed. `False` if the move was illegal. |
| is_promotion | bool | Whether the move results in a pending pawn promotion (requiring the player to choose a piece). |
| new_status | GameStatus | The game status after the move (e.g., ACTIVE, CHECK, CHECKMATE). Only meaningful when `success` is `True`. |

---

## 14. Move Attempt

A data transfer object created by `InputController` when a player completes a drag-and-drop action. Passed to `GameController.attempt_move()` for validation and execution.

| Attribute | Type | Description |
|-----------|------|-------------|
| start_pos | Position | The board position the piece was picked up from. |
| end_pos | Position | The board position the piece was dropped on. |
