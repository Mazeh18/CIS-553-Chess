# Use Case Model

## Actors

| Actor | Description |
|-------|-------------|
| Player | A human user interacting with the chess application. Two players (White and Black) share the same machine, taking turns. |

---

## Use Case Diagram (Text Representation)

```
                        +------------------------------------------+
                        |           Chess Application              |
                        |                                          |
                        |   +----------------------------+         |
   +--------+           |   | UC-01: Launch Application  |         |
   |        |---------->|   +----------------------------+         |
   | Player |           |                                          |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-02: View Credits        |         |
   |        |           |   +----------------------------+         |
   |        |           |                                          |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-03: Select Time Control |         |
   |        |           |   +----------------------------+         |
   |        |           |              |                           |
   |        |           |              v                           |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-04: Play Game           |         |
   |        |           |   +----------------------------+         |
   |        |           |        |           |       |             |
   |        |           |        v           v       v             |
   |        |           |   +--------+ +--------+ +--------+      |
   |        |           |   | UC-05  | | UC-06  | | UC-07  |      |
   |        |           |   | Move   | | Capture| | Special|      |
   |        |           |   | Piece  | | Piece  | | Move   |      |
   |        |           |   +--------+ +--------+ +--------+      |
   |        |           |                                          |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-08: Promote Pawn        |         |
   |        |           |   +----------------------------+         |
   |        |           |                                          |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-09: Undo Move           |         |
   |        |           |   +----------------------------+         |
   |        |           |                                          |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-10: Resign              |         |
   |        |           |   +----------------------------+         |
   |        |           |                                          |
   |        |---------->|   +----------------------------+         |
   |        |           |   | UC-11: Start New Game      |         |
   |        |           |   +----------------------------+         |
   |        |           |                                          |
   +--------+           +------------------------------------------+
```

---

## Use Case Descriptions

---

### UC-01: Launch Application

| Field | Description |
|-------|-------------|
| **Name** | Launch Application |
| **Actor** | Player |
| **Preconditions** | Python and required dependencies are installed. |
| **Postconditions** | The start menu is displayed with Play, Credits, and Exit buttons. |
| **Main Flow** | 1. The player runs the application. 2. The system displays the start menu with the game title and three buttons: Play, Credits, Exit. |
| **Alternate Flow** | If the player clicks Exit, the application closes. |

---

### UC-02: View Credits

| Field | Description |
|-------|-------------|
| **Name** | View Credits |
| **Actor** | Player |
| **Preconditions** | The start menu is displayed. |
| **Postconditions** | The player has viewed the credits and returned to the start menu. |
| **Main Flow** | 1. The player clicks the Credits button on the start menu. 2. The system displays the credits screen showing the author(s) of the application. 3. The player clicks the Back button. 4. The system returns to the start menu. |

---

### UC-03: Select Time Control

| Field | Description |
|-------|-------------|
| **Name** | Select Time Control |
| **Actor** | Player |
| **Preconditions** | The start menu is displayed. |
| **Postconditions** | A time control is selected and the game begins. |
| **Main Flow** | 1. The player clicks the Play button on the start menu. 2. The system displays the time control selection screen with preset options: Bullet (2+1), Blitz (5+0), Classic (10+5), Rapid (30+20), No Time, and Custom. 3. The player clicks one of the preset options. 4. The system starts a new game with the selected time control. |
| **Alternate Flow A** | The player selects Custom: 1. The system displays input fields for time (minutes) and increment (seconds). 2. The player enters values and clicks Start. 3. The system validates the input and starts the game. |
| **Alternate Flow B** | The player clicks Back to return to the start menu. |

---

### UC-04: Play Game

| Field | Description |
|-------|-------------|
| **Name** | Play Game |
| **Actor** | Player |
| **Preconditions** | A time control has been selected. |
| **Postconditions** | The game is active with the board displayed, clocks running (if applicable), and White to move. |
| **Main Flow** | 1. The system displays the game screen: board (White's perspective), clocks, empty move history, empty captured pieces, and action buttons. 2. White's clock starts (if time control is active). 3. The players alternate turns by dragging and dropping pieces. 4. After each move: the turn switches, the move is recorded, clocks update, and captured pieces / point advantage update. 5. The game continues until checkmate, stalemate, draw, resignation, or timeout. 6. The system displays the game result. Only New Game is available as an action. |

---

### UC-05: Move Piece (Drag and Drop)

| Field | Description |
|-------|-------------|
| **Name** | Move Piece |
| **Actor** | Player |
| **Preconditions** | A game is active. It is the player's turn. |
| **Postconditions** | The piece is moved to the destination. Turn switches. Clock updates. |
| **Main Flow** | 1. The player presses and holds the mouse button on one of their pieces. 2. The system picks up the piece: it follows the cursor, and legal destination squares are highlighted. 3. The player drags the piece to a legal destination square. 4. The player releases the mouse button. 5. The system places the piece on the destination square. 6. The system records the move in move history. 7. The system applies the increment to the moving player's clock (if applicable). 8. The system switches the turn to the other player. 9. The system checks for check, checkmate, stalemate, or draw conditions. |
| **Alternate Flow A** | The player releases the piece on an invalid square or off the board — the piece returns to its original position. No move is made. |
| **Alternate Flow B** | The player releases on a square with an opponent's piece — triggers UC-06 (Capture). |
| **Alternate Flow C** | The move results in pawn promotion — triggers UC-08 (Promote Pawn). |

---

### UC-06: Capture Piece

| Field | Description |
|-------|-------------|
| **Name** | Capture Piece |
| **Actor** | Player (via UC-05) |
| **Preconditions** | A piece is being dropped on a square occupied by an opponent's piece. |
| **Postconditions** | The opponent's piece is captured and removed. The capturing piece occupies the square. Point advantage is updated. |
| **Main Flow** | 1. The player drops their piece on a valid square containing an opponent's piece (extends UC-05). 2. The system removes the opponent's piece from the board. 3. The system adds the captured piece to the capturing player's captured list. 4. The system recalculates and updates the point advantage display. 5. Normal post-move processing continues (clock, turn switch). |

---

### UC-07: Perform Special Move

| Field | Description |
|-------|-------------|
| **Name** | Perform Special Move |
| **Actor** | Player (via UC-05) |
| **Preconditions** | Conditions for the specific special move are met. |
| **Postconditions** | The special move is executed correctly. |

#### UC-07a: Castling

| Field | Description |
|-------|-------------|
| **Main Flow** | 1. The player picks up their King. 2. Legal moves include castling squares if all conditions are met: kingside (placing the King next to the rook on h1/h8) or queenside (placing the King next to the rook on a1/a8). 3. The player drops the King on the castling square. 4. The system moves the King two squares toward the Rook. 5. The system automatically moves the Rook to the other side of the King. |

#### UC-07b: En Passant

| Field | Description |
|-------|-------------|
| **Main Flow** | 1. The opponent has performed a starting pawn move of two squares forward and lands next to the player's pawn 2. The player picks up their pawn. 3. The en passant capture square is shown as a legal move. 4. The player drops the pawn on the en passant square. 5. The system places the pawn diagonally behind the opponent's pawn and removes the opponent's pawn from its square. |

---

### UC-08: Promote Pawn

| Field | Description |
|-------|-------------|
| **Name** | Promote Pawn |
| **Actor** | Player |
| **Preconditions** | A pawn has been dropped on the opponent's back rank. |
| **Postconditions** | The pawn is replaced by the selected piece. |
| **Main Flow** | 1. A pawn move reaches the 8th rank (White) or 1st rank (Black). 2. The system pauses the game and displays the promotion popup with four options: Queen, Rook, Bishop, Knight. 3. The player clicks one of the options. 4. The system replaces the pawn on the board with the chosen piece. 5. The game resumes — turn switches, clocks update. |

---

### UC-09: Undo Move

| Field | Description |
|-------|-------------|
| **Name** | Undo Move |
| **Actor** | Player |
| **Preconditions** | At least one move has been made. The game is still active. |
| **Postconditions** | The board, clocks, and all state are restored to before the last move. |
| **Main Flow** | 1. The player clicks the Undo button. 2. The system reverses the last move: the piece returns to its origin, any captured piece is restored, and flags (castling rights, en passant, has_moved) are reverted. 3. The system restores the clock to the time recorded before the move. 4. The last entry is removed from the move history. 5. The turn switches back. |
| **Alternate Flow** | If no moves have been made, the Undo button is disabled. |

---

### UC-10: Resign

| Field | Description |
|-------|-------------|
| **Name** | Resign |
| **Actor** | Player |
| **Preconditions** | A game is active. |
| **Postconditions** | The game ends. The resigning player loses. |
| **Main Flow** | 1. The player clicks the Resign button. 2. The system ends the game and declares the other player the winner. 3. The system displays the result in the status area. The board remains visible. 4. Only the New Game button is available. |

---

### UC-11: Start New Game

| Field | Description |
|-------|-------------|
| **Name** | Start New Game |
| **Actor** | Player |
| **Preconditions** | The player is on the game screen (during or after a game). |
| **Postconditions** | The player is returned to the time control selection screen. |
| **Main Flow** | 1. The player clicks the New Game button. 2. The system navigates to the time control selection screen (UC-03). 3. The player selects a time control and a fresh game begins. |
---
### UC-12: Exit Game
| Field | Description |
|-------|-------------|
| **Name** | close the game |
| **Actor** | Player |
| **Preconditions** | The player is on title screen |
| **Postconditions** | the game is closed |
| **Main Flow** | 1. The player clicks the exit game button. 2. The game closes itself down
---
### UC-13: Set Custom Settings for time control
| Field | Description |
|-------|-------------|
| **Name** | Set Custom time Control |
| **Actor** | Player |
| **Preconditions** | The player is on Custom time screen |
| **Postconditions** | the game starts with the custom time|
| **Main Flow** | 1. The player inputs the total time in minuts. 2.  The player inputs the total time increment in seconds. 3. player hits the start button 4. game validates inputs to make sure they are valid or sets default max or minimum values
