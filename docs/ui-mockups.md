# UI Mockups

> **Note**: These are text-based wireframes. For high-fidelity visual mockups, use a tool such as Figma or draw.io.

---

## Screen 1: Start Menu

The first screen displayed when the application launches.

```
+-----------------------------------------------+
|                                                |
|                                                |
|                                                |
|              ♚  CHESS  ♔                       |
|                                                |
|                                                |
|             +----------------+                 |
|             |      Play      |                 |
|             +----------------+                 |
|                                                |
|             +----------------+                 |
|             |    Credits     |                 |
|             +----------------+                 |
|                                                |
|             +----------------+                 |
|             |      Exit      |                 |
|             +----------------+                 |
|                                                |
|                                                |
+-----------------------------------------------+
```

- **Play**: Navigates to the time control selection screen.
- **Credits**: Navigates to the credits screen.
- **Exit**: Closes the application.

---

## Screen 2: Credits

```
+-----------------------------------------------+
|                                                |
|                  Credits                       |
|                                                |
|                                                |
|             Developed by:                      |
|             [Author Name]                      |
|                                                |
|                                                |
|             +----------------+                 |
|             |      Back      |                 |
|             +----------------+                 |
|                                                |
+-----------------------------------------------+
```

- **Back**: Returns to the start menu.

---

## Screen 3: Time Control Selection

Displayed after clicking "Play" on the start menu.

```
+-----------------------------------------------+
|                                                |
|            Select Time Control                 |
|                                                |
|   +----------+  +----------+  +----------+    |
|   | Bullet   |  | Blitz    |  | Rapid    |    |
|   |  2 + 1   |  |  5 + 0   |  | 10 + 5   |    |
|   +----------+  +----------+  +----------+    |
|                                                |
|   +----------+  +----------+  +----------+    |
|   | Rapid    |  | No Time  |  | Custom   |    |
|   | 30 + 20  |  |   --     |  |  ...     |    |
|   +----------+  +----------+  +----------+    |
|                                                |
|                                                |
|             +----------------+                 |
|             |      Back      |                 |
|             +----------------+                 |
|                                                |
+-----------------------------------------------+
```

- Clicking a preset starts the game immediately with that time control.
- **Custom** expands input fields for minutes and increment:

```
|   Custom Time Control:                         |
|   Time (min):  [____]   Increment (sec): [____]|
|                                                |
|             +----------------+                 |
|             |     Start      |                 |
|             +----------------+                 |
```

- **Back**: Returns to the start menu.

---

## Screen 4: Main Game Screen

The primary game interface. Layout shown from White's perspective (before first flip).

```
+------------------------------------------------------------------------+
|                                                                        |
|   BLACK  ♚                                            05:00            |
|   Captured: ♙♙♗               Point Advantage: +2                     |
|                                                                        |
|     a    b    c    d    e    f    g    h                                |
|   +----+----+----+----+----+----+----+----+   +----------------------+ |
| 8 | bR | bN | bB | bQ | bK | bB | bN | bR |   | Move History         | |
|   +----+----+----+----+----+----+----+----+   |                      | |
| 7 | bP | bP | bP | bP | bP | bP | bP | bP |   | 1. e4    e5         | |
|   +----+----+----+----+----+----+----+----+   | 2. Nf3   Nc6        | |
| 6 |    |    |    |    |    |    |    |    |   | 3. Bb5   a6         | |
|   +----+----+----+----+----+----+----+----+   | 4. Ba4   ...        | |
| 5 |    |    |    |    |    |    |    |    |   |                      | |
|   +----+----+----+----+----+----+----+----+   |                      | |
| 4 |    |    |    |    |    |    |    |    |   |                      | |
|   +----+----+----+----+----+----+----+----+   |                      | |
| 3 |    |    |    |    |    |    |    |    |   |                      | |
|   +----+----+----+----+----+----+----+----+   |                      | |
| 2 | wP | wP | wP | wP | wP | wP | wP | wP |   |                      | |
|   +----+----+----+----+----+----+----+----+   |                      | |
| 1 | wR | wN | wB | wQ | wK | wB | wN | wR |   +----------------------+ |
|   +----+----+----+----+----+----+----+----+                            |
|     a    b    c    d    e    f    g    h                                |
|                                                                        |
|   WHITE  ♔                                            05:00            |
|   Captured: ♟♞                Point Advantage: --                      |
|                                                                        |
|   Turn: WHITE              [ Undo ]  [ Resign ]  [ New Game ]          |
|                                                                        |
+------------------------------------------------------------------------+
```

### Layout Description

| Region | Position | Content |
|--------|----------|---------|
| Opponent Info | Top | Opponent's name/color, their clock, their captured pieces and point advantage. |
| Chessboard | Center-left | 8x8 board with rank/file labels. Alternating light/dark squares. |
| Move History | Center-right | Scrollable panel of moves in algebraic notation (move number, white, black). |
| Current Player Info | Bottom-above-status | Current player's name/color, their clock, their captured pieces and point advantage. |
| Status / Actions | Bottom | Turn indicator and action buttons (Undo, Resign, New Game). |

### Board Flip Behavior

After White makes a move, the board flips so Black's pieces are at the bottom:

```
|     h    g    f    e    d    c    b    a      |
|   +----+----+----+----+----+----+----+----+  |
| 1 | wR | wN | wB | wK | wQ | wB | wN | wR | |
|   +----+----+----+----+----+----+----+----+  |
| 2 | wP | wP | wP | wP | wP | wP | wP | wP | |
|   +----+----+----+----+----+----+----+----+  |
|   ...                                        |
| 7 | bP | bP | bP | bP | bP | bP | bP | bP | |
|   +----+----+----+----+----+----+----+----+  |
| 8 | bR | bN | bB | bQ | bK | bB | bN | bR | |
|   +----+----+----+----+----+----+----+----+  |
|     h    g    f    e    d    c    b    a      |
```

The current player's info and clock is always at the bottom. The opponent's info is always at the top.

---

## Screen 5: Drag and Drop Interaction

While the player holds a piece, the piece follows the cursor and legal moves are highlighted.

```
|   +----+----+----+----+----+----+----+----+
| 4 |    |    |    |    | ** |    |    |    |     ** = legal move dot
|   +----+----+----+----+----+----+----+----+
| 3 |    |    |    |    | ** |    |    |    |     ** = legal move dot
|   +----+----+----+----+----+----+----+----+
| 2 | wP | wP | wP | wP | ~~ | wP | wP | wP |   ~~ = origin square
|   +----+----+----+----+----+----+----+----+         (empty, piece
                    ♙ <-- piece follows cursor         is being held)
```

- The origin square is shown empty (or with a subtle highlight).
- Legal destination squares display a dot or circle overlay.
- Squares with capturable enemy pieces show a ring/border highlight.
- The dragged piece is rendered at the mouse cursor position, above all other elements.

---

## Screen 6: Pawn Promotion Popup

When a pawn reaches the back rank, a popup appears over the board.

```
  +---------------------------+
  |     Choose Promotion      |
  |                           |
  |   +-----+  +-----+       |
  |   |  ♛  |  |  ♜  |       |
  |   |Queen|  |Rook |       |
  |   +-----+  +-----+       |
  |                           |
  |   +-----+  +-----+       |
  |   |  ♝  |  |  ♞  |       |
  |   |Bshp |  |Knght|       |
  |   +-----+  +-----+       |
  |                           |
  +---------------------------+
```

- Modal popup — the game is paused until the player selects a piece.
- Icons match the current player's color.

---

## Screen 7: Game Over State

The game result is displayed in the status area. The board is NOT blocked.

```
+------------------------------------------------------------------------+
|                                                                        |
|   (board remains fully visible with final position)                    |
|                                                                        |
|   +-------------------------------------------------+                  |
|   | Checkmate! White wins.         [ New Game ]      |                  |
|   +-------------------------------------------------+                  |
|                                                                        |
+------------------------------------------------------------------------+
```

Possible messages:
- "Checkmate! [Color] wins."
- "Stalemate — Draw."
- "Draw by insufficient material."
- "Draw by threefold repetition."
- "Draw by fifty-move rule."
- "[Color] resigned. [Other color] wins."
- "[Color] ran out of time. [Other color] wins."

The **New Game** button is the only action available. Undo and Resign are disabled/hidden.

---

## Color Scheme

| Element | Color |
|---------|-------|
| Light squares | Beige (#F0D9B5) |
| Dark squares | Brown (#B58863) |
| Legal move dots | Gray, semi-transparent |
| Capture highlight | Red tint, semi-transparent |
| Selected/origin square | Light blue (#646FD4, semi-transparent) |
| Check highlight on King | Red (#E84040, semi-transparent) |
| Background | Dark gray (#312E2B) |
| Side panels | Slightly lighter gray (#3C3A37) |
| Text | White (#FFFFFF) |
| Buttons | Rounded, neutral gray with hover effect |
| Start menu background | Dark gradient |
