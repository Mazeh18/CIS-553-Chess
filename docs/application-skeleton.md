# Application Skeleton

This document maps the project's file structure, describes the role of each module, and traces how control flows through the application.

See also: [System Architecture](system-architecture.md) | [Class Diagram](class-diagram.md) | [Control Classes](control-classes.md) | [Boundary Classes](boundary-classes.md)

---

## Directory Structure

```
CIS-553-Chess/
├── main.py                              # Entry point — Pygame init, game loop
├── requirements.txt                     # Dependencies: pygame, black, pytest
├── pyproject.toml                       # Black + pytest configuration
│
├── docs/                                # Requirements and design documents
│   ├── functional-requirements.md
│   ├── non-functional-requirements.md
│   ├── use-case-model.md
│   ├── data-dictionary.md
│   ├── class-diagram.md
│   ├── boundary-classes.md
│   ├── control-classes.md
│   ├── sequence-diagrams.md
│   ├── dialog-map.md
│   ├── ui-mockups.md
│   ├── system-architecture.md
│   ├── application-skeleton.md
│   └── test-cases.md
│
├── src/
│   ├── constants.py                     # Colors, fonts, button sizes, layout values
│   │
│   ├── entities/                        # Data layer — pure data, no logic, no UI
│   │   ├── enums.py                     # ScreenType, Color, PieceType, GameStatus
│   │   ├── piece.py                     # Piece: type, color, has_moved, value, icon
│   │   ├── board.py                     # Board: 8x8 grid, execute_move, undo_move, clone
│   │   ├── position.py                  # Position: row/col with algebraic conversion
│   │   ├── move.py                      # Move: piece, positions, captured, special flags
│   │   ├── move_attempt.py              # MoveAttempt: start_pos + end_pos (UI → logic)
│   │   ├── move_result.py               # MoveResult: success, is_promotion, new_status (logic → UI)
│   │   ├── game_state.py                # GameState: board + status + captures + pending_promotion
│   │   ├── time_control.py              # TimeControl: name, minutes, increment, presets
│   │   ├── captured_pieces.py           # CapturedPieces: tracked per player, point advantage
│   │   └── drag_state.py                # DragState: piece, origin, mouse_pos, legal_moves
│   │
│   ├── controllers/                     # Logic layer — game rules, no UI
│   │   ├── game_controller.py           # Orchestrator: attempt_move, attempt_promotion, undo
│   │   ├── move_validator.py            # Legality: piece rules, check filtering, castling, en passant
│   │   ├── draw_detector.py             # Draws: insufficient material, repetition, 50-move
│   │   ├── notation_controller.py       # Algebraic notation: Nf3, O-O, exd5, e8=Q
│   │   ├── input_controller.py          # Mouse events → MoveAttempt via DragState
│   │   └── screen_navigation_controller.py  # Screen transitions: START_MENU ↔ CREDITS ↔ TIME_SELECT ↔ GAME
│   │
│   ├── screens/                         # UI layer — Pygame rendering
│   │   ├── base_screen.py               # Abstract base: handle_event, update, draw
│   │   ├── start_menu_screen.py         # Play, Credits, Exit buttons
│   │   ├── credits_screen.py            # Author info + Back button
│   │   ├── time_select_screen.py        # 6 presets + custom entry + Back
│   │   └── game_screen.py               # Board, pieces, drag-and-drop, undo, promotion popup
│   │
│   └── components/                      # Reusable UI widgets
│       ├── button.py                    # Button: label, rect, hover, disabled, on_click
│       ├── text_input.py                # TextInput: numeric entry for custom time
│       └── promotion_popup.py           # PromotionPopup: modal 4-piece selection overlay
│
└── tests/                               # Unit tests (pytest)
    ├── conftest.py                      # Shared fixtures: empty_board, standard_board, validator
    ├── test_pawn_moves.py               # Pawn: forward, double, blocked, capture, en passant
    ├── test_rook_moves.py               # Rook: sliding, blocking, capture
    ├── test_bishop_moves.py             # Bishop: diagonals, blocking, capture
    ├── test_queen_moves.py              # Queen: combined movement, blocking, capture
    ├── test_knight_moves.py             # Knight: L-shape, jumping, corners
    ├── test_king_moves.py               # King: adjacent, can't enter check
    ├── test_castling.py                 # Castling: valid/invalid, execution, undo, notation
    ├── test_en_passant.py               # En passant: valid/invalid, execution, undo
    ├── test_promotion.py                # Promotion: flow, all 4 types, capture, notation
    ├── test_check_detection.py          # Check, checkmate, stalemate detection
    ├── test_draw_detection.py           # Insufficient material, repetition, 50-move
    ├── test_notation.py                 # Algebraic notation for all move types
    ├── test_board.py                    # Board: execute, undo, clone, position hash
    └── test_undo.py                     # Undo: basic, captures, multiple, status restore
```

---

## Module Descriptions

### Entry Point

#### `main.py`

Initializes Pygame, creates a fullscreen display surface, and runs the game loop:

```
pygame.init()
surface = pygame.display.set_mode(FULLSCREEN)
nav_controller = ScreenNavigationController(surface)

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        current_screen.handle_event(event)
    current_screen.update(dt)
    current_screen.draw()
    pygame.display.flip()
```

---

### Entity Modules

| Module | Key Class | Attributes | Purpose |
|--------|-----------|------------|---------|
| `enums.py` | `Color`, `PieceType`, `GameStatus`, `ScreenType` | Enum values | Type-safe constants used throughout |
| `piece.py` | `Piece` | `piece_type`, `color`, `has_moved` | Single chess piece with value and display icon |
| `board.py` | `Board` | `squares[8][8]`, `current_turn`, `move_history`, `halfmove_clock`, `position_history` | Core board state with move execution and undo |
| `position.py` | `Position` | `row`, `col` | Board coordinate with algebraic conversion, hashable |
| `move.py` | `Move` | `piece`, `had_moved`, `start_pos`, `end_pos`, `captured_piece`, `is_castling`, `is_en_passant`, `promotion_piece`, `notation` | Complete move record for execution and undo |
| `move_attempt.py` | `MoveAttempt` | `start_pos`, `end_pos` | Input DTO from UI to logic |
| `move_result.py` | `MoveResult` | `success`, `is_promotion`, `new_status` | Output DTO from logic to UI |
| `game_state.py` | `GameState` | `status`, `winner`, `board`, `time_control`, `captured_pieces`, `pending_promotion` | Top-level game container |
| `time_control.py` | `TimeControl` | `name`, `time_minutes`, `increment_seconds` | Time control preset or custom configuration |
| `captured_pieces.py` | `CapturedPieces` | `white_captured`, `black_captured` | Tracks captured pieces and point advantage |
| `drag_state.py` | `DragState` | `is_dragging`, `piece`, `origin`, `mouse_pos`, `legal_moves` | Current drag-and-drop interaction state |

---

### Controller Modules

| Module | Key Class | Key Methods | Purpose |
|--------|-----------|-------------|---------|
| `game_controller.py` | `GameController` | `new_game()`, `attempt_move()`, `attempt_promotion()`, `undo_last_move()`, `resign()` | Central orchestrator — connects validation, execution, notation, and draw detection |
| `move_validator.py` | `MoveValidator` | `get_legal_moves()`, `is_in_check()`, `is_checkmate()`, `is_stalemate()` | All move legality including special moves (castling, en passant) and check filtering |
| `draw_detector.py` | `DrawDetector` | `check_draw_conditions()`, `is_insufficient_material()`, `is_threefold_repetition()`, `is_fifty_move_rule()` | Draw condition detection |
| `notation_controller.py` | `NotationController` | `generate_notation()`, `needs_disambiguation()` | Standard algebraic notation generation |
| `input_controller.py` | `InputController` | `handle_mouse_down()`, `handle_mouse_motion()`, `handle_mouse_up()` | Mouse event translation to game actions |
| `screen_navigation_controller.py` | `ScreenNavigationController` | `navigate_to_start_menu()`, `navigate_to_credits()`, `navigate_to_time_select()`, `navigate_to_game()` | Screen lifecycle and transitions |

---

### Screen Modules

| Module | Key Class | Composes | Signals |
|--------|-----------|----------|---------|
| `base_screen.py` | `BaseScreen` (abstract) | — | `handle_event()`, `update()`, `draw()` |
| `start_menu_screen.py` | `StartMenuScreen` | 3 Buttons | `on_play`, `on_credits`, `on_exit` |
| `credits_screen.py` | `CreditsScreen` | 1 Button | `on_back` |
| `time_select_screen.py` | `TimeSelectScreen` | 7 Buttons, 2 TextInputs | `on_time_selected(minutes, increment)`, `on_back` |
| `game_screen.py` | `GameScreen` | InputController, DragState, PromotionPopup, 2 Buttons, MoveHistoryPanel, CapturedPiecesDisplay | Delegates to `GameController` |

---

### Component Modules

| Module | Key Class | Purpose |
|--------|-----------|---------|
| `button.py` | `Button` | Clickable rectangle with label, hover highlight, disabled state |
| `text_input.py` | `TextInput` | Numeric text field for custom time control entry |
| `promotion_popup.py` | `PromotionPopup` | Modal overlay showing Queen/Rook/Bishop/Knight options for pawn promotion |

---

## Control Flow Traces

### Application Launch → Start Menu

```
main.py
  → ScreenNavigationController.__init__(surface)
    → navigate_to_start_menu()
      → StartMenuScreen(surface, on_play, on_credits, on_exit)
  → game loop begins
```

### Play → Time Select → Game Start

```
Player clicks "Play"
  → StartMenuScreen.on_play callback
    → ScreenNavigationController.navigate_to_time_select()
      → TimeSelectScreen(surface, on_time_selected, on_back)

Player clicks "Blitz 5+0"
  → TimeSelectScreen.on_time_selected(5, 0)
    → ScreenNavigationController._handle_time_selected(5, 0)
      → TimeControl("5+0", 5, 0)
      → navigate_to_game(time_control)
        → GameController.new_game(time_control)
          → Board.initialize_standard()
          → GameState(board, time_control)
        → GameScreen(surface, game_controller, on_back)
```

### Move Piece (Drag-and-Drop)

```
Player mouse_down on own piece
  → GameScreen.handle_event(MOUSEBUTTONDOWN)
    → InputController.handle_mouse_down(pixel_pos, board)
      → pixel_to_board_position → Position
      → GameController.get_legal_moves(position)
        → MoveValidator.get_legal_moves(board, position)
      → DragState.start_drag(piece, origin, legal_moves)

Player mouse_motion
  → InputController.handle_mouse_motion(pixel_pos)
    → DragState.update_mouse(pixel_pos)
  → GameScreen.draw() renders piece at cursor

Player mouse_up on valid square
  → InputController.handle_mouse_up(pixel_pos)
    → DragState.reset()
    → return MoveAttempt(origin, target)
  → GameController.attempt_move(attempt)
    → validate, detect specials, execute, notation, switch turn, check status
    → return MoveResult
```

### Undo Move

```
Player clicks "Undo" button
  → GameScreen._on_undo()
    → GameController.undo_last_move()
      → Board.undo_move()
        → restore piece to start, revert has_moved
        → handle en passant / castling / promotion undo
      → CapturedPieces.remove_last_captured()
      → recalculate status (ACTIVE or CHECK)
```

---

## Configuration

### `pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ["py38"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### `requirements.txt`

```
pygame>=2.5.0
black
pytest
```

### `src/constants.py`

Centralizes all UI constants: window title, FPS (60), color palette, font sizes, button dimensions, and board highlight colors. Screens and components import from here rather than hardcoding values.
