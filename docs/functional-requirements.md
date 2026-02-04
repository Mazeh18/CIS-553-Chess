# Functional Requirements

## Project Overview

A desktop chess application built in Python with a graphical user interface. The game supports two human players on the same machine with drag-and-drop controls, time controls, and board flipping between turns.

---

## FR-01: Start Menu

- **FR-01.1**: Upon launching the application, the system shall display a start menu screen.
- **FR-01.2**: The start menu shall contain three buttons: **Play**, **Credits**, and **Exit**.
- **FR-01.3**: The **Exit** button shall close the application.

## FR-02: Credits Screen

- **FR-02.1**: Clicking the **Credits** button shall navigate to a credits screen.
- **FR-02.2**: The credits screen shall display the names of the application's authors.
- **FR-02.3**: The credits screen shall provide a **Back** button to return to the start menu.

## FR-03: Time Control Selection

- **FR-03.1**: Clicking the **Play** button shall navigate to a time control selection screen.
- **FR-03.2**: The time control selection screen shall offer the following preset options:
  | Option | Time (minutes) | Increment (seconds) |
  |--------|---------------|---------------------|
  | Bullet | 2 | 1 |
  | Blitz | 5 | 0 |
  | Rapid | 10 | 5 |
  | Rapid | 30 | 20 |
  | No Time | -- | -- |
- **FR-03.3**: The system shall offer a **Custom** option allowing the player to specify a custom time (in minutes) and increment (in seconds).
- **FR-03.4**: Selecting a time control option (or confirming a custom one) shall start a new game with that time setting.

## FR-04: Game Initialization

- **FR-04.1**: The system shall display a standard 8x8 chessboard with all 32 pieces in their starting positions.
- **FR-04.2**: White shall always move first.
- **FR-04.3**: If a time control is selected (not "No Time"), each player's clock shall be initialized to the chosen time.

## FR-05: Board Orientation / Flipping

- **FR-05.1**: At the start of the game, the board shall be oriented from White's perspective (White pieces at the bottom).
- **FR-05.2**: After each completed move, the board shall flip orientation so that the current player's pieces are at the bottom of the screen.

## FR-06: Piece Interaction (Drag and Drop)

- **FR-06.1**: The player shall initiate a move by pressing and holding the mouse button on one of their own pieces.
- **FR-06.2**: While holding, the piece shall visually follow the mouse cursor (dragged).
- **FR-06.3**: While holding, the system shall highlight all legal destination squares for the held piece.
- **FR-06.4**: Releasing the mouse button on a valid destination square shall execute the move.
- **FR-06.5**: Releasing the mouse button on an invalid square or off the board shall cancel the move and return the piece to its original square.
- **FR-06.6**: The system shall only allow the current player to pick up their own colored pieces.

## FR-07: Piece Movement Rules

- **FR-07.1**: The system shall enforce legal movement rules for each piece type:
  - **Pawn**: One square forward, two squares forward from the starting rank, diagonal capture.
  - **Rook**: Any number of squares horizontally or vertically.
  - **Bishop**: Any number of squares diagonally.
  - **Queen**: Any number of squares horizontally, vertically, or diagonally.
  - **King**: One square in any direction.
  - **Knight**: L-shaped move (two squares + one square perpendicular). May jump over pieces.
- **FR-07.2**: The system shall prevent pieces (except Knights) from moving through occupied squares.
- **FR-07.3**: The system shall prevent moves that leave the current player's King in check.

## FR-08: Capturing

- **FR-08.1**: A piece shall capture an opponent's piece by being dropped on its square.
- **FR-08.2**: The captured piece shall be removed from the board.
- **FR-08.3**: The system shall display captured pieces for each player, grouped by color.
- **FR-08.4**: The system shall calculate and display a **point advantage** based on standard piece values (Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9).

## FR-09: Special Moves

- **FR-09.1 Castling**: The system shall allow castling (kingside and queenside) when:
  - Neither the King nor the involved Rook has previously moved.
  - No pieces are between the King and the Rook.
  - The King is not in check.
  - The King does not pass through or land on a square under attack.
  - Castling is executed by dragging the King two squares toward the Rook; the Rook moves automatically.
- **FR-09.2 En Passant**: The system shall allow en passant capture when:
  - The opponent's pawn just advanced two squares from its starting rank.
  - The capturing pawn is on its 5th rank and adjacent to the opponent's pawn.
  - The capture occurs on the immediately following turn.
- **FR-09.3 Pawn Promotion**: When a pawn reaches the opponent's back rank:
  - The system shall display a popup dialog with promotion options: Queen, Rook, Bishop, Knight.
  - The game shall pause until the player selects a piece.
  - The pawn shall be replaced by the selected piece.

## FR-10: Check, Checkmate, and Stalemate

- **FR-10.1**: The system shall detect when a King is in check and visually indicate it.
- **FR-10.2**: When in check, only moves that resolve the check shall be legal.
- **FR-10.3**: The system shall detect **checkmate** and end the game, declaring the opponent the winner.
- **FR-10.4**: The system shall detect **stalemate** and end the game as a draw.

## FR-11: Draw Conditions

- **FR-11.1**: The system shall detect a draw by **stalemate** (no legal moves, not in check).
- **FR-11.2**: The system shall detect a draw by **insufficient material** (e.g., K vs K, K+B vs K, K+N vs K).
- **FR-11.3**: The system shall detect a draw by **threefold repetition** (same position three times, same player to move).
- **FR-11.4**: The system shall detect a draw by the **fifty-move rule** (50 consecutive moves without a pawn move or capture).

## FR-12: Time Controls

- **FR-12.1**: When a time control is active, each player's clock shall count down during their turn.
- **FR-12.2**: After a player completes a move, their clock shall receive the increment (if any).
- **FR-12.3**: If a player's clock reaches 0:00, that player loses the game on time.
- **FR-12.4**: Both clocks shall be displayed on screen at all times.
- **FR-12.5**: When "No Time" is selected, no clocks shall be displayed or enforced.

## FR-13: Turn Management

- **FR-13.1**: The system shall alternate turns between White and Black after each valid move.
- **FR-13.2**: The system shall display whose turn it is at all times.

## FR-14: Move History

- **FR-14.1**: The system shall maintain and display a move history in standard algebraic notation.
- **FR-14.2**: The move history shall be displayed in a panel on the game screen.

## FR-15: Game Actions

- **FR-15.1**: The system shall provide an **Undo** button that reverses the last move and restores the previous board state (including timers, castling rights, en passant status).
- **FR-15.2**: The system shall provide a **Resign** button. Clicking it ends the game with a loss for the resigning player.
- **FR-15.3**: The system shall provide a **New Game** button that returns the player to the time control selection screen.

## FR-16: Game Over

- **FR-16.1**: When the game ends (checkmate, stalemate, draw, resignation, or timeout), the system shall display the result.
- **FR-16.2**: The only action available after the game ends shall be **New Game**.
- **FR-16.3**: The game-over indication shall **not** block the player's view of the board. The final board position must remain visible.
