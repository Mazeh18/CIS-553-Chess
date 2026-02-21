# Entity Class Diagram

This document defines the entity classes for the chess application. Entity classes hold data and basic behavior only — no UI code, no complex game rules. They map directly from the [Data Dictionary](data-dictionary.md).

---

## Class Diagram

```mermaid
classDiagram
    direction TB

    %% ── Enumerations ──

    class ScreenType {
        <<enumeration>>
        START_MENU
        CREDITS
        TIME_SELECT
        GAME
    }

    class Color {
        <<enumeration>>
        WHITE
        BLACK
        +opposite() Color
    }

    class PieceType {
        <<enumeration>>
        PAWN
        ROOK
        KNIGHT
        BISHOP
        QUEEN
        KING
    }

    class GameStatus {
        <<enumeration>>
        ACTIVE
        CHECK
        CHECKMATE
        STALEMATE
        DRAW_INSUFFICIENT_MATERIAL
        DRAW_THREEFOLD_REPETITION
        DRAW_FIFTY_MOVE
        RESIGNED
        TIMEOUT
        +is_game_over() bool
        +is_draw() bool
    }

    %% ── Data Classes ──

    class Position {
        +int row
        +int col
        +to_algebraic() str
        +from_algebraic(notation: str)$ Position
        +is_valid() bool
        +__eq__(other) bool
        +__hash__() int
    }

    class Piece {
        +PieceType piece_type
        +Color color
        +bool has_moved
        +value() int
        +symbol() str
    }

    class Move {
        +Piece piece
        +Position start_pos
        +Position end_pos
        +Piece? captured_piece
        +bool is_castling
        +bool is_en_passant
        +PieceType? promotion_piece
        +str notation
        +float? time_after_move
    }

    class TimeControl {
        +str name
        +int? time_minutes
        +int increment_seconds
        +is_timed() bool
        +get_starting_seconds() float
    }

    class MoveHistoryEntry {
        +int move_number
        +str white_move
        +str? black_move
        +from_move_list(moves: list~Move~)$ list~MoveHistoryEntry~
    }

    %% ── Data Transfer Types ──

    class MoveResult {
        +bool success
        +bool is_promotion
        +GameStatus new_status
    }

    class MoveAttempt {
        +Position start_pos
        +Position end_pos
    }

    %% ── Stateful Classes ──

    class Board {
        +Piece?[][] squares
        +Color current_turn
        +list~Move~ move_history
        +int halfmove_clock
        +int fullmove_number
        +list~str~ position_history
        +initialize_standard() void
        +get_piece(pos: Position) Piece?
        +set_piece(pos: Position, piece: Piece?) void
        +execute_move(move: Move) void
        +undo_move() Move
        +switch_turn() void
        +get_position_hash() str
        +find_king(color: Color) Position
        +get_pieces_by_color(color: Color) list~tuple~
        +clone() Board
    }

    class Clock {
        +float white_time
        +float black_time
        +int increment
        +bool is_running
        +Color? active_color
        +bool enabled
        +get_time(color: Color) float
        +tick(delta: float) void
        +add_increment(color: Color) void
        +start(color: Color) void
        +stop() void
        +is_time_expired(color: Color) bool
        +format_time(color: Color) str
    }

    class GameState {
        +GameStatus status
        +Color? winner
        +Board board
        +Clock clock
        +TimeControl time_control
        +CapturedPieces captured_pieces
        +is_game_over() bool
        +get_result_message() str
    }

    class CapturedPieces {
        +list~Piece~ white_captured
        +list~Piece~ black_captured
        +add_captured(piece: Piece) void
        +remove_last_captured(color: Color) Piece
        +get_points(color: Color) int
        +get_point_advantage() int
    }

    class DragState {
        +bool is_dragging
        +Piece? piece
        +Position? origin
        +tuple? mouse_pos
        +list~Position~ legal_moves
        +start_drag(piece: Piece, origin: Position, moves: list~Position~) void
        +update_mouse(pos: tuple) void
        +cancel_drag() void
        +reset() void
    }

    %% ── Relationships ──

    GameState *-- Board : composes
    GameState *-- Clock : composes
    GameState *-- TimeControl : composes
    GameState *-- CapturedPieces : composes
    GameState --> GameStatus : status

    Board --> Color : current_turn
    Board o-- "0..32" Piece : squares
    Board o-- "0..*" Move : move_history

    Move --> Piece : piece (moved)
    Move --> Piece : captured_piece
    Move --> Position : start_pos
    Move --> Position : end_pos
    Move --> PieceType : promotion_piece

    Piece --> PieceType : piece_type
    Piece --> Color : color

    CapturedPieces o-- "0..*" Piece : white_captured
    CapturedPieces o-- "0..*" Piece : black_captured

    DragState --> Piece : piece
    DragState --> Position : origin
    DragState o-- "0..*" Position : legal_moves

    MoveHistoryEntry --> Move : from_move_list

    MoveResult --> GameStatus : new_status
    MoveAttempt --> Position : start_pos
    MoveAttempt --> Position : end_pos

    Clock --> Color : active_color
    TimeControl --> ScreenType : used during TIME_SELECT
```

---

## Class Descriptions

### Enumerations

| Enum | Purpose | Notes |
|------|---------|-------|
| `ScreenType` | Identifies which screen is currently displayed | Values: START_MENU, CREDITS, TIME_SELECT, GAME |
| `Color` | Identifies player/piece color | `opposite()` returns BLACK for WHITE and vice versa |
| `PieceType` | Identifies the type of chess piece | Standard six piece types |
| `GameStatus` | Tracks the current game status | `is_game_over()` returns true for CHECKMATE, STALEMATE, all draws, RESIGNED, TIMEOUT. `is_draw()` returns true for STALEMATE and DRAW_* values. |

### Data Classes (Immutable / Value Types)

| Class | Purpose |
|-------|---------|
| `Position` | Represents a square on the board (row 0-7, col 0-7). Supports algebraic notation conversion and equality/hashing for use in sets and dicts. |
| `Piece` | Represents a single chess piece with its type, color, and move history. `value()` returns standard point value. `symbol()` returns unicode character. |
| `Move` | Represents a single move with all metadata needed for undo (captured piece, special move flags, clock time). |
| `TimeControl` | Represents a time control preset. `is_timed()` returns false when time_minutes is None. `get_starting_seconds()` converts minutes to seconds. |
| `MoveHistoryEntry` | Display-oriented pairing of white and black moves for the move history panel. `from_move_list()` converts raw Move list to display entries. |
| `MoveResult` | Returned by GameController after a move attempt. Indicates success, whether promotion is needed, and the resulting game status. |
| `MoveAttempt` | Input to GameController from InputController. Pairs a start and end position for move validation. |

### Stateful Classes

| Class | Purpose |
|-------|---------|
| `Board` | The 8x8 game board. Holds pieces in a 2D array, tracks turns, move history, and position history for draw detection. `clone()` creates a deep copy for move validation without mutating game state. |
| `Clock` | Manages both players' chess clocks. `tick()` decrements the active player's time. `add_increment()` adds the increment after a move. `format_time()` returns a display string (e.g., "05:00"). |
| `GameState` | Top-level game container. Composes Board, Clock, TimeControl, and CapturedPieces. `get_result_message()` returns a human-readable result string (e.g., "Checkmate! White wins."). |
| `CapturedPieces` | Tracks captured pieces for both players. `get_points()` sums point values. `get_point_advantage()` returns the difference. |
| `DragState` | Tracks the current drag-and-drop interaction. `start_drag()` captures the piece, origin, and legal moves. `cancel_drag()` restores state if dropped on an invalid square. |
