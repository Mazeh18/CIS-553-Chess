# Boundary Classes

This document identifies the boundary (UI) classes for the chess application. Boundary classes handle Pygame rendering and user input detection. They read from entity classes for display and emit signals/callbacks to control classes for processing.

See also: [Entity Class Diagram](class-diagram.md) | [Control Classes](control-classes.md) | [UI Mockups](ui-mockups.md)

---

## Screen-Level Boundaries

One screen-level boundary is active at a time, corresponding to the current `ScreenType` value. Each screen owns its child components and delegates rendering and input handling to them.

| Boundary Class | Screen | ScreenType | Composes | Key Signals |
|---|---|---|---|---|
| `StartMenuScreen` | Start Menu | `START_MENU` | Button x3 (Play, Credits, Exit) | `on_play`, `on_credits`, `on_exit` |
| `CreditsScreen` | Credits | `CREDITS` | Button x1 (Back) | `on_back` |
| `TimeSelectScreen` | Time Control | `TIME_SELECT` | Button x7 (6 presets + Back), CustomTimeView | `on_time_selected(TimeControl)`, `on_custom`, `on_back` |
| `CustomTimeView` | Custom Time (sub-state of TimeSelectScreen) | `TIME_SELECT` | TextInput x2 (Minutes, Increment), Button x2 (Start, Back) | `on_start(minutes, increment)`, `on_back` |
| `GameScreen` | Main Game | `GAME` | Composite — see sub-components below | Delegates to sub-components |

---

## Screen Details

### StartMenuScreen

**Mockup Reference**: [Screen 1: Start Menu](ui-mockups.md#screen-1-start-menu)

| Element | Type | Behavior |
|---------|------|----------|
| Title | Label | Displays "CHESS" with chess piece icons |
| Play button | Button | Emits `on_play` → navigates to TimeSelectScreen |
| Credits button | Button | Emits `on_credits` → navigates to CreditsScreen |
| Exit button | Button | Emits `on_exit` → closes application |

**Reads From**: None (static content)

---

### CreditsScreen

**Mockup Reference**: [Screen 2: Credits](ui-mockups.md#screen-2-credits)

| Element | Type | Behavior |
|---------|------|----------|
| Title | Label | Displays "Credits" |
| Author info | Label | Displays author names |
| Back button | Button | Emits `on_back` → navigates to StartMenuScreen |

**Reads From**: None (static content)

---

### TimeSelectScreen

**Mockup Reference**: [Screen 3: Time Control Selection](ui-mockups.md#screen-3-time-control-selection)

Has two visual sub-states managed internally:

1. **PresetSelection** (default) — Shows the 6 time control option buttons and a Back button.
2. **CustomTimeEntry** — Shows the CustomTimeView with text inputs for minutes and increment.

| Element | Type | Behavior |
|---------|------|----------|
| Title | Label | Displays "Select Time Control" |
| Bullet button | Button | Emits `on_time_selected(Bullet 2+1)` |
| Blitz button | Button | Emits `on_time_selected(Blitz 5+0)` |
| Rapid button | Button | Emits `on_time_selected(Rapid 10+5)` |
| Classic button | Button | Emits `on_time_selected(Classic 30+20)` |
| No Time button | Button | Emits `on_time_selected(No Time)` |
| Custom button | Button | Switches to CustomTimeEntry sub-state |
| Back button | Button | Emits `on_back` → navigates to StartMenuScreen |

**Reads From**: Preset `TimeControl` definitions

---

### CustomTimeView

**Mockup Reference**: [Screen 3: Custom section](ui-mockups.md#screen-3-time-control-selection)

Embedded within `TimeSelectScreen` when the Custom option is selected.

| Element | Type | Behavior |
|---------|------|----------|
| Title | Label | Displays "Custom Time Control" |
| Minutes input | TextInput | Numeric input for time in minutes |
| Increment input | TextInput | Numeric input for increment in seconds |
| Start button | Button | Validates input, emits `on_start(minutes, increment)` |
| Back button | Button | Emits `on_back` → returns to PresetSelection sub-state |

**Reads From**: User input (TextInput values)

---

### GameScreen

**Mockup Reference**: [Screen 4: Main Game Screen](ui-mockups.md#screen-4-main-game-screen)

The GameScreen is a composite boundary that delegates to specialized sub-components. It owns the layout and coordinates rendering order.

**Reads From**: `GameState`, `DragState`

---

## Game Screen Sub-Components

These boundary components are composed within `GameScreen` and each renders a specific region of the game interface. Most are implemented as private draw methods within `GameScreen` (e.g., `_draw_move_history()`, `_draw_captured_pieces()`, `_draw_status()`). `PromotionPopup` is a standalone component in `src/components/promotion_popup.py`.

| Boundary Class | Region | Reads From | Writes To |
|---|---|---|---|
| `BoardRenderer` | Center-left | `Board`, `DragState` | Renders board squares, pieces, drag highlights, legal move dots, check highlight |
| `ClockDisplay` (x2) | Top-right / Bottom-right | `Clock` | Renders formatted time for one player; highlights active clock |
| `CapturedPiecesDisplay` (x2) | Near player info areas | `CapturedPieces` | Renders captured piece icons for one player |
| `PointAdvantageDisplay` (x2) | Near captured pieces | `CapturedPieces` | Renders point advantage value (e.g., "+2") for the leading player |
| `MoveHistoryPanel` | Right side | `list[MoveHistoryEntry]` | Renders scrollable move list in algebraic notation |
| `StatusBar` | Bottom bar | `GameState` | Renders turn indicator ("Turn: WHITE") or result message |
| `ActionButtonBar` | Bottom bar | `GameState` | Renders action buttons (Undo, Resign, New Game, Main Menu); adjusts visibility based on game state |
| `PromotionPopup` | Modal overlay on board | `PieceType` selection | Renders 4 promotion piece options; captures click selection |

---

## Sub-Component Details

### BoardRenderer

**Mockup Reference**: [Screen 4](ui-mockups.md#screen-4-main-game-screen) (board area), [Screen 5](ui-mockups.md#screen-5-drag-and-drop-interaction)

| Rendering Layer | Description |
|-----------------|-------------|
| Square colors | Alternating beige (#F0D9B5) and brown (#B58863) squares |
| Rank/file labels | Labels a-h (columns) and 1-8 (rows) along board edges |
| Pieces | Piece images positioned on their squares |
| Origin highlight | Light blue highlight on the square a piece was picked up from |
| Legal move dots | Gray semi-transparent dots on valid destination squares |
| Capture highlights | Red tint on squares with capturable enemy pieces |
| Check highlight | Red highlight on the king's square when in check |
| Dragged piece | Piece rendered at mouse cursor position, above all other layers |

**Reads From**: `Board` (piece positions), `DragState` (drag highlights and legal moves)

---

### ClockDisplay

**Mockup Reference**: [Screen 4](ui-mockups.md#screen-4-main-game-screen) (time displays: "05:00")

Instantiated twice — once for White (bottom-right), once for Black (top-right).

| Element | Description |
|---------|-------------|
| Time value | Formatted as MM:SS (zero-padded, e.g., "05:00") |
| Active indicator | Visual emphasis (bold / highlight) when it is this player's turn |
| Hidden state | Not rendered when `Clock.enabled` is false (No Time games) |

**Reads From**: `Clock.get_time(color)`, `Clock.format_time(color)`, `Clock.active_color`

---

### CapturedPiecesDisplay

Instantiated twice — once per player.

| Element | Description |
|---------|-------------|
| Piece icons | Small piece images in a row, sorted by value |

**Reads From**: `CapturedPieces.white_captured` or `CapturedPieces.black_captured`

---

### PointAdvantageDisplay

Instantiated twice — shown only for the player with the advantage.

| Element | Description |
|---------|-------------|
| Advantage text | Displays "+N" where N is the point difference, or nothing if equal |

**Reads From**: `CapturedPieces.get_point_advantage()`

---

### MoveHistoryPanel

**Mockup Reference**: [Screen 4](ui-mockups.md#screen-4-main-game-screen) (right side panel)

| Element | Description |
|---------|-------------|
| Header | "Move History" label |
| Move rows | Each row: move number, white move notation, black move notation |
| Scrolling | Auto-scrolls to the most recent move |

**Reads From**: `list[MoveHistoryEntry]` (generated from `Board.move_history`)

---

### StatusBar

**Mockup Reference**: [Screen 4](ui-mockups.md#screen-4-main-game-screen) (bottom: "Turn: WHITE")

| State | Display |
|-------|---------|
| Game active | "Turn: WHITE" or "Turn: BLACK" |
| Game over | Result message from `GameState.get_result_message()` |

**Reads From**: `GameState.status`, `GameState.get_result_message()`

---

### ActionButtonBar

**Mockup Reference**: [Screen 4](ui-mockups.md#screen-4-main-game-screen) (bottom: Undo, Resign, New Game), [Screen 7](ui-mockups.md#screen-7-game-over-state)

| Button | State: Game Active | State: Game Over |
|--------|-------------------|-----------------|
| Undo | Enabled (if moves exist) | Disabled/Hidden |
| Resign | Enabled | Disabled/Hidden |
| New Game | Disabled/Hidden | Enabled |
| Main Menu | Enabled | Enabled |

**Signals**: `on_undo`, `on_resign`, `on_new_game`, `on_main_menu`

---

### PromotionPopup

**Mockup Reference**: [Screen 6: Pawn Promotion Popup](ui-mockups.md#screen-6-pawn-promotion-popup)

| Element | Description |
|---------|-------------|
| Title | "Choose Promotion" |
| Queen button | Piece icon + label, emits `on_promote(QUEEN)` |
| Rook button | Piece icon + label, emits `on_promote(ROOK)` |
| Bishop button | Piece icon + label, emits `on_promote(BISHOP)` |
| Knight button | Piece icon + label, emits `on_promote(KNIGHT)` |

**Behavior**: Modal overlay — blocks all other input until a selection is made. Piece icons match the promoting player's color.

**Reads From**: Current player's `Color`
**Signals**: `on_promote(PieceType)`

---

## Reusable UI Components

These are generic widgets used across multiple boundary classes.

### Button

| Attribute | Type | Description |
|-----------|------|-------------|
| `label` | str | Display text |
| `rect` | pygame.Rect | Position and size |
| `enabled` | bool | Whether the button is interactive |
| `hovered` | bool | Whether the mouse is over the button |
| `on_click` | callback | Function called when clicked |

**Visual Style**: Rounded rectangle, neutral gray background, hover highlight, disabled state (dimmed).

---

### TextInput

| Attribute | Type | Description |
|-----------|------|-------------|
| `label` | str | Field label displayed above/beside the input |
| `value` | str | Current text content |
| `rect` | pygame.Rect | Position and size |
| `focused` | bool | Whether this input has keyboard focus |
| `numeric_only` | bool | When true, only allows digit characters |

**Visual Style**: Underlined input field with label. Cursor blink when focused. Numeric filtering for time control inputs.

---

## Boundary-to-Screen Mapping

Cross-reference verifying every UI mockup screen has a corresponding boundary class:

| UI Mockup Screen | Boundary Class |
|-----------------|----------------|
| Screen 1: Start Menu | `StartMenuScreen` |
| Screen 2: Credits | `CreditsScreen` |
| Screen 3: Time Control Selection | `TimeSelectScreen` + `CustomTimeView` |
| Screen 4: Main Game Screen | `GameScreen` (with all sub-components) |
| Screen 5: Drag and Drop | `BoardRenderer` (within `GameScreen`) |
| Screen 6: Pawn Promotion | `PromotionPopup` (within `GameScreen`) |
| Screen 7: Game Over | `StatusBar` + `ActionButtonBar` (within `GameScreen`) |
