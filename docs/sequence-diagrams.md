# Sequence Diagrams

This document contains UML sequence diagrams illustrating the interactions between actors, boundary classes, control classes, and entity classes for each use case in the chess application.

See also: [Use Case Model](use-case-model.md) | [Boundary Classes](boundary-classes.md) | [Control Classes](control-classes.md) | [Entity Class Diagram](class-diagram.md) | [Dialog Map](dialog-map.md)

---

## Diagram Index

| Diagram | Use Cases Covered |
|---------|-------------------|
| [1. Application Launch and Navigation](#1-application-launch-and-navigation-uc-01-uc-02-uc-11) | UC-01, UC-02, UC-11 |
| [2. Time Control Selection and Game Initialization](#2-time-control-selection-and-game-initialization-uc-03-uc-04) | UC-03, UC-04 |
| [3. Move Piece and Capture](#3-move-piece-and-capture-uc-05-uc-06) | UC-05, UC-06 |
| [4. Castling](#4-castling-uc-07a) | UC-07a |
| [5. En Passant](#5-en-passant-uc-07b) | UC-07b |
| [6. Pawn Promotion](#6-pawn-promotion-uc-08) | UC-08 |
| [7. Undo Move](#7-undo-move-uc-09) | UC-09 |
| [8. Resign](#8-resign-uc-10) | UC-10 |
| [9. Game End Conditions](#9-game-end-conditions) | Post-move checks |

---

## 1. Application Launch and Navigation (UC-01, UC-02, UC-11)

Covers launching the application, viewing credits, exiting, and starting a new game from the game screen.

```mermaid
sequenceDiagram
    actor Player
    participant SMS as StartMenuScreen
    participant CS as CreditsScreen
    participant SNC as ScreenNavigationController
    participant ABB as ActionButtonBar

    Note over Player, SNC: UC-01: Launch Application
    Player ->> SMS: run application
    SMS ->> SNC: initialize(START_MENU)
    SNC -->> SMS: current_screen = START_MENU
    SMS -->> Player: render Play, Credits, Exit buttons

    Note over Player, SNC: UC-02: View Credits
    Player ->> SMS: click Credits button
    SMS ->> SNC: on_credits → navigate_to_credits()
    SNC -->> CS: current_screen = CREDITS
    CS -->> Player: render author information, Back button
    Player ->> CS: click Back button
    CS ->> SNC: on_back → navigate_to_start_menu()
    SNC -->> SMS: current_screen = START_MENU
    SMS -->> Player: render start menu

    Note over Player, SNC: UC-01 Alternate: Exit Application
    Player ->> SMS: click Exit button
    SMS ->> SNC: on_exit → handle_exit()
    SNC -->> Player: application closes

    Note over Player, ABB: UC-11: Start New Game (from Game Screen)
    Player ->> ABB: click New Game button
    ABB ->> SNC: on_new_game → navigate_to_time_select()
    SNC -->> Player: current_screen = TIME_SELECT
```

---

## 2. Time Control Selection and Game Initialization (UC-03, UC-04)

Covers selecting a time control (preset or custom) and initializing a new game.

```mermaid
sequenceDiagram
    actor Player
    participant TSS as TimeSelectScreen
    participant CTV as CustomTimeView
    participant SNC as ScreenNavigationController
    participant GC as GameController
    participant CC as ClockController
    participant Board as Board
    participant Clock as Clock
    participant CP as CapturedPieces
    participant GState as GameState
    participant GS as GameScreen

    Note over Player, GS: UC-03: Select Time Control (Preset)
    Player ->> TSS: click preset (e.g., Blitz 5+0)
    TSS ->> SNC: on_time_selected(TimeControl{5, 0})
    SNC ->> GC: navigate_to_game(TimeControl) → new_game(TimeControl)

    Note over GC, GState: UC-04: Game Initialization
    GC ->> Board: initialize_standard()
    Board -->> GC: 32 pieces in starting positions
    GC ->> CC: initialize(TimeControl)
    CC ->> Clock: set white_time, black_time, increment, enabled
    GC ->> CP: create empty captured lists
    GC ->> GState: status = ACTIVE, current_turn = WHITE, winner = None
    SNC -->> GS: current_screen = GAME
    GS -->> Player: render board, clocks, empty move history, action buttons
    GC ->> CC: start_clock(WHITE)
    CC ->> Clock: start(WHITE)
    Clock -->> CC: active_color = WHITE, is_running = true

    Note over Player, CTV: UC-03 Alternate: Custom Time Control
    Player ->> TSS: click Custom button
    TSS ->> CTV: switch to CustomTimeEntry sub-state
    CTV -->> Player: render minutes input, increment input, Start, Back
    Player ->> CTV: enter minutes=15, increment=10, click Start
    CTV ->> SNC: on_start(15, 10) → on_time_selected(TimeControl{15, 10})
    SNC ->> GC: navigate_to_game(TimeControl) → new_game(TimeControl)
    Note over GC: (same initialization as preset flow above)

    Note over Player, TSS: UC-03 Alternate: Back to Start Menu
    Player ->> TSS: click Back button
    TSS ->> SNC: on_back → navigate_to_start_menu()
    SNC -->> Player: current_screen = START_MENU
```

---

## 3. Move Piece and Capture (UC-05, UC-06)

Covers the core drag-and-drop move flow, including normal moves and captures, with full post-move processing.

```mermaid
sequenceDiagram
    actor Player
    participant GS as GameScreen
    participant BR as BoardRenderer
    participant IC as InputController
    participant DS as DragState
    participant GC as GameController
    participant MV as MoveValidator
    participant Board as Board
    participant NC as NotationController
    participant CC as ClockController
    participant Clock as Clock
    participant DD as DrawDetector
    participant CP as CapturedPieces
    participant GState as GameState
    participant MHP as MoveHistoryPanel
    participant SB as StatusBar

    Note over Player, SB: UC-05: Drag Start — Pick Up Piece
    Player ->> GS: mouse_down on own piece
    GS ->> IC: handle_mouse_down(pixel_pos, Board)
    IC ->> IC: pixel_to_board_position(pixel_pos) → Position
    IC ->> GC: get_legal_moves(Position)
    GC ->> MV: get_legal_moves(Board, Position)
    MV ->> MV: _get_[piece]_moves(Board, Position)
    MV ->> MV: _filter_check_moves(Board, moves, Color)
    MV -->> GC: list[Position] (legal destinations)
    GC -->> IC: legal destinations
    IC ->> DS: start_drag(Piece, Position, list[Position])
    DS -->> IC: is_dragging = true
    GS ->> BR: render(Board, DragState)
    BR -->> Player: highlight origin (blue), show legal move dots, capture highlights

    Note over Player, DS: UC-05: Dragging — Piece Follows Cursor
    Player ->> GS: mouse_motion
    GS ->> IC: handle_mouse_motion(pixel_pos)
    IC ->> DS: update_mouse(pixel_pos)
    GS ->> BR: render(Board, DragState)
    BR -->> Player: piece follows cursor

    Note over Player, SB: UC-05: Drop — Execute Move
    Player ->> GS: mouse_up on valid square
    GS ->> IC: handle_mouse_up(pixel_pos)
    IC ->> IC: pixel_to_board_position(pixel_pos) → Position
    IC -->> GC: MoveAttempt(start_pos, end_pos)
    IC ->> DS: reset()

    GC ->> MV: get_legal_moves(Board, start_pos)
    MV -->> GC: validate end_pos is in legal moves

    opt UC-06: Capture — opponent piece on destination
        GC ->> Board: get_piece(end_pos)
        Board -->> GC: captured_piece (Piece)
        GC ->> CP: add_captured(captured_piece)
        CP ->> CP: recalculate get_point_advantage()
    end

    GC ->> Board: execute_move(Move)
    Board ->> Board: set_piece(end_pos, piece), set_piece(start_pos, None)
    Board ->> Board: piece.has_moved = true
    Board ->> Board: update halfmove_clock, fullmove_number
    Board ->> Board: get_position_hash() → add to position_history
    GC ->> NC: generate_notation(Board, Move)
    NC ->> NC: needs_disambiguation(Board, Move)
    NC -->> GC: notation string (e.g., "Nf3", "exd5")
    GC ->> Board: add Move to move_history
    GC ->> CC: switch_turn(current_color)
    CC ->> Clock: add_increment(current_color)
    CC ->> Clock: start(opponent_color)
    GC ->> Board: switch_turn()
    Board -->> GC: current_turn = opponent_color

    Note over GC, DD: Post-Move Status Checks
    GC ->> MV: is_in_check(Board, opponent_color)
    MV -->> GC: check result (bool)
    GC ->> MV: is_checkmate(Board, opponent_color)
    MV -->> GC: checkmate result (bool)
    GC ->> MV: is_stalemate(Board, opponent_color)
    MV -->> GC: stalemate result (bool)
    GC ->> DD: check_draw_conditions(Board)
    DD ->> DD: is_insufficient_material(Board)
    DD ->> DD: is_threefold_repetition(Board)
    DD ->> DD: is_fifty_move_rule(Board)
    DD -->> GC: GameStatus or None
    GC ->> GState: update status, winner

    GC -->> GS: MoveResult(success, is_promotion, new_status)
    GS ->> BR: render(Board, DragState)
    GS ->> MHP: render(Board.move_history)
    GS ->> SB: render(GameState)
    GS -->> Player: updated board, move history, clocks, status

    Note over Player, DS: UC-05 Alternate: Invalid Drop
    Player ->> GS: mouse_up on invalid square
    GS ->> IC: handle_mouse_up(pixel_pos)
    IC ->> IC: pixel_to_board_position(pixel_pos) → Position
    IC ->> DS: cancel_drag()
    DS ->> DS: reset()
    IC -->> GC: None (no MoveAttempt)
    GS ->> BR: render(Board, DragState)
    BR -->> Player: piece returns to original square
```

---

## 4. Castling (UC-07a)

Covers both kingside and queenside castling with precondition validation.

```mermaid
sequenceDiagram
    actor Player
    participant GS as GameScreen
    participant IC as InputController
    participant DS as DragState
    participant GC as GameController
    participant MV as MoveValidator
    participant Board as Board
    participant NC as NotationController
    participant CC as ClockController
    participant Clock as Clock

    Note over Player, Clock: UC-07a: Castling
    Player ->> GS: mouse_down on King
    GS ->> IC: handle_mouse_down(pixel_pos, Board)
    IC ->> GC: get_legal_moves(king_position)
    GC ->> MV: get_legal_moves(Board, king_position)
    MV ->> MV: _get_king_moves(Board, king_position)
    MV ->> MV: _get_castling_moves(Board, king_position)

    Note over MV: Castling Precondition Checks (FR-09.1)
    MV ->> Board: get_piece(king_pos) → King.has_moved == false
    MV ->> Board: get_piece(rook_pos) → Rook.has_moved == false
    MV ->> MV: verify no pieces between King and Rook
    MV ->> MV: is_in_check(Board, color) → false
    MV ->> MV: is_square_attacked(Board, transit_square, opponent) → false
    MV ->> MV: is_square_attacked(Board, destination, opponent) → false

    MV -->> GC: legal moves (includes castling destination)
    GC -->> IC: legal destinations
    IC ->> DS: start_drag(King, king_position, legal_moves)
    GS -->> Player: highlight legal squares including castling square

    Player ->> GS: mouse_up on castling square
    GS ->> IC: handle_mouse_up(pixel_pos)
    IC -->> GC: MoveAttempt(king_pos, castling_square)
    IC ->> DS: reset()

    GC ->> Board: execute_move(Move{is_castling=true})
    Note over Board: King moves 2 squares toward Rook
    Board ->> Board: set_piece(king_destination, King)
    Board ->> Board: King.has_moved = true
    Note over Board: Rook auto-moves to other side of King
    Board ->> Board: set_piece(rook_destination, Rook)
    Board ->> Board: Rook.has_moved = true

    GC ->> NC: generate_notation(Board, Move)
    NC -->> GC: "O-O" (kingside) or "O-O-O" (queenside)
    GC ->> Board: add Move to move_history
    GC ->> CC: switch_turn(color)
    CC ->> Clock: add_increment(color)
    CC ->> Clock: start(opponent_color)
    GC ->> Board: switch_turn()
    GC ->> GC: post-move checks (check, checkmate, stalemate, draw)
    GC -->> GS: MoveResult
    GS -->> Player: updated board with castled position
```

---

## 5. En Passant (UC-07b)

Covers the en passant capture, including the prerequisite opponent pawn advance.

```mermaid
sequenceDiagram
    actor Player
    participant GS as GameScreen
    participant IC as InputController
    participant DS as DragState
    participant GC as GameController
    participant MV as MoveValidator
    participant Board as Board
    participant CP as CapturedPieces
    participant NC as NotationController
    participant CC as ClockController
    participant Clock as Clock

    Note over Player, Clock: Precondition: Opponent just moved pawn 2 squares forward

    Player ->> GS: mouse_down on own pawn (5th rank, adjacent to opponent pawn)
    GS ->> IC: handle_mouse_down(pixel_pos, Board)
    IC ->> GC: get_legal_moves(pawn_position)
    GC ->> MV: get_legal_moves(Board, pawn_position)
    MV ->> MV: _get_pawn_moves(Board, pawn_position)

    Note over MV: En Passant Check (FR-09.2)
    MV ->> Board: get last Move from move_history
    Board -->> MV: last_move (opponent pawn advanced 2 squares)
    MV ->> MV: verify own pawn on 5th rank
    MV ->> MV: verify opponent pawn is adjacent
    MV ->> MV: verify this is the immediately following turn

    MV -->> GC: legal moves (includes en passant capture square)
    GC -->> IC: legal destinations
    IC ->> DS: start_drag(Pawn, pawn_position, legal_moves)
    GS -->> Player: highlight legal squares including en passant square

    Player ->> GS: mouse_up on en passant square
    GS ->> IC: handle_mouse_up(pixel_pos)
    IC -->> GC: MoveAttempt(pawn_pos, en_passant_square)
    IC ->> DS: reset()

    GC ->> Board: execute_move(Move{is_en_passant=true})
    Note over Board: Pawn placed diagonally behind opponent's pawn
    Board ->> Board: set_piece(en_passant_square, Pawn)
    Board ->> Board: set_piece(pawn_origin, None)
    Note over Board: Opponent's pawn removed from its square
    Board ->> Board: set_piece(opponent_pawn_pos, None)
    Board -->> GC: captured_piece = opponent's pawn

    GC ->> CP: add_captured(opponent_pawn)
    CP ->> CP: recalculate get_point_advantage()
    GC ->> NC: generate_notation(Board, Move)
    NC -->> GC: notation (e.g., "exd6")
    GC ->> Board: add Move to move_history
    GC ->> CC: switch_turn(color)
    CC ->> Clock: add_increment(color)
    CC ->> Clock: start(opponent_color)
    GC ->> Board: switch_turn()
    GC ->> GC: post-move checks (check, checkmate, stalemate, draw)
    GC -->> GS: MoveResult
    GS -->> Player: updated board, captured pieces display
```

---

## 6. Pawn Promotion (UC-08)

Covers the pawn promotion flow with the modal promotion popup.

```mermaid
sequenceDiagram
    actor Player
    participant GS as GameScreen
    participant IC as InputController
    participant DS as DragState
    participant GC as GameController
    participant MV as MoveValidator
    participant Board as Board
    participant CC as ClockController
    participant Clock as Clock
    participant PP as PromotionPopup
    participant NC as NotationController
    participant DD as DrawDetector
    participant GState as GameState
    participant SB as StatusBar

    Note over Player, SB: UC-08: Pawn Promotion

    Player ->> GS: mouse_up (pawn dropped on back rank)
    GS ->> IC: handle_mouse_up(pixel_pos)
    IC -->> GC: MoveAttempt(pawn_pos, back_rank_square)
    IC ->> DS: reset()

    GC ->> MV: get_legal_moves(Board, pawn_pos)
    MV -->> GC: back_rank_square is legal
    GC ->> Board: execute_move(Move) — pawn placed on back rank
    GC ->> CC: stop_clock()
    CC ->> Clock: stop()
    GC ->> GState: set pending_promotion = true

    GC -->> GS: MoveResult(success=true, is_promotion=true)
    GS ->> PP: display(player_color)
    PP -->> Player: show Queen, Rook, Bishop, Knight options (modal)

    Player ->> PP: click Queen
    PP ->> GC: on_promote(QUEEN) → attempt_promotion(QUEEN)
    GC ->> Board: replace pawn with Queen at back_rank_square
    Board ->> Board: set_piece(back_rank_square, Piece{QUEEN, color})
    GC ->> NC: generate_notation(Board, Move)
    NC -->> GC: notation (e.g., "e8=Q")
    GC ->> Board: add Move to move_history

    GC ->> CC: switch_turn(color)
    CC ->> Clock: add_increment(color)
    CC ->> Clock: start(opponent_color)
    GC ->> Board: switch_turn()

    Note over GC, DD: Post-Promotion Checks
    GC ->> MV: is_in_check(Board, opponent_color)
    MV -->> GC: check result
    GC ->> MV: is_checkmate(Board, opponent_color)
    MV -->> GC: checkmate result
    GC ->> MV: is_stalemate(Board, opponent_color)
    MV -->> GC: stalemate result
    GC ->> DD: check_draw_conditions(Board)
    DD -->> GC: draw status or None
    GC ->> GState: update status, winner

    GC -->> GS: MoveResult(success=true, is_promotion=false, new_status)
    GS ->> PP: hide()
    GS ->> SB: render(GameState)
    GS -->> Player: updated board with promoted piece, game continues
```

---

## 7. Undo Move (UC-09)

Covers reversing the last move and restoring all associated state.

```mermaid
sequenceDiagram
    actor Player
    participant ABB as ActionButtonBar
    participant GC as GameController
    participant Board as Board
    participant CP as CapturedPieces
    participant CC as ClockController
    participant Clock as Clock
    participant MV as MoveValidator
    participant GState as GameState
    participant GS as GameScreen
    participant BR as BoardRenderer
    participant MHP as MoveHistoryPanel
    participant SB as StatusBar

    Note over Player, SB: UC-09: Undo Move

    Player ->> ABB: click Undo button
    ABB ->> GC: on_undo → undo_last_move()

    GC ->> Board: undo_move()
    Board ->> Board: retrieve last Move from move_history
    Board ->> Board: set_piece(Move.start_pos, Move.piece) — return piece to origin
    Board ->> Board: set_piece(Move.end_pos, None) — clear destination
    Board ->> Board: Move.piece.has_moved = revert flag

    opt Captured piece exists (Move.captured_piece != None)
        Board ->> Board: set_piece(Move.end_pos, Move.captured_piece) — restore captured piece
        GC ->> CP: remove_last_captured(opponent_color)
        CP ->> CP: recalculate get_point_advantage()
    end

    opt Move was castling (Move.is_castling == true)
        Board ->> Board: set_piece(rook_original_pos, Rook) — return Rook to origin
        Board ->> Board: set_piece(rook_castled_pos, None) — clear Rook destination
        Board ->> Board: Rook.has_moved = false
    end

    opt Move was en passant (Move.is_en_passant == true)
        Board ->> Board: set_piece(opponent_pawn_pos, opponent_pawn) — restore captured pawn
        GC ->> CP: remove_last_captured(opponent_color)
    end

    opt Move was promotion (Move.promotion_piece != None)
        Board ->> Board: set_piece(Move.start_pos, original_pawn) — replace promoted piece with pawn
    end

    Board ->> Board: remove last entry from move_history
    Board ->> Board: switch_turn() — revert to previous player
    Board ->> Board: revert halfmove_clock, fullmove_number
    Board ->> Board: remove last entry from position_history

    GC ->> CC: restore clock from Move.time_after_move
    CC ->> Clock: set time values from saved state

    GC ->> MV: is_in_check(Board, current_turn)
    MV -->> GC: recalculated check status
    GC ->> GState: update status (ACTIVE or CHECK)

    GC -->> GS: undo complete
    GS ->> BR: render(Board, DragState)
    GS ->> MHP: render(Board.move_history)
    GS ->> SB: render(GameState)
    GS -->> Player: board restored to previous state
```

---

## 8. Resign (UC-10)

Covers the resignation flow and game-over transition.

```mermaid
sequenceDiagram
    actor Player
    participant ABB as ActionButtonBar
    participant GC as GameController
    participant CC as ClockController
    participant Clock as Clock
    participant GState as GameState
    participant GS as GameScreen
    participant SB as StatusBar

    Note over Player, SB: UC-10: Resign

    Player ->> ABB: click Resign button
    ABB ->> GC: on_resign → resign(current_color)
    GC ->> GState: status = RESIGNED
    GC ->> GState: winner = opponent_color
    GC ->> CC: stop_clock()
    CC ->> Clock: stop()
    Clock -->> CC: is_running = false

    GC -->> GS: game over
    GS ->> SB: render(GameState)
    SB ->> GState: get_result_message()
    GState -->> SB: "White resigned. Black wins!"
    SB -->> Player: display result message
    GS ->> ABB: render(GameState)
    ABB -->> Player: Undo disabled, Resign disabled, New Game enabled
```

---

## 9. Game End Conditions

Covers the post-move checks performed after every move and the per-frame clock timeout check.

```mermaid
sequenceDiagram
    participant GC as GameController
    participant MV as MoveValidator
    participant DD as DrawDetector
    participant Board as Board
    participant CC as ClockController
    participant Clock as Clock
    participant GState as GameState
    participant GS as GameScreen
    participant SB as StatusBar
    participant ABB as ActionButtonBar
    actor Player

    Note over GC, Board: After Each Move — Status Checks
    GC ->> MV: is_in_check(Board, opponent_color)
    MV -->> GC: in_check (bool)

    alt Opponent is in check
        GC ->> MV: is_checkmate(Board, opponent_color)
        MV -->> GC: is_checkmate (bool)
        alt Checkmate detected
            GC ->> GState: status = CHECKMATE, winner = current_color
            GC ->> CC: stop_clock()
            CC ->> Clock: stop()
        else Check only (not checkmate)
            GC ->> GState: status = CHECK
        end
    else Opponent is NOT in check
        GC ->> MV: is_stalemate(Board, opponent_color)
        MV -->> GC: is_stalemate (bool)
        alt Stalemate detected
            GC ->> GState: status = STALEMATE, winner = None
            GC ->> CC: stop_clock()
            CC ->> Clock: stop()
        else Not stalemate — check draw conditions
            GC ->> DD: check_draw_conditions(Board)
            DD ->> DD: is_insufficient_material(Board)
            DD ->> DD: is_threefold_repetition(Board)
            DD ->> DD: is_fifty_move_rule(Board)
            DD -->> GC: GameStatus (DRAW_*) or None
            alt Draw detected
                GC ->> GState: status = DRAW_*, winner = None
                GC ->> CC: stop_clock()
                CC ->> Clock: stop()
            else Game continues
                GC ->> GState: status = ACTIVE
            end
        end
    end

    alt Game over (any end condition met)
        GC -->> GS: MoveResult(new_status = game_over)
        GS ->> SB: render(GameState)
        SB ->> GState: get_result_message()
        GState -->> SB: result string (e.g., "Checkmate! White wins.")
        SB -->> Player: display result message
        GS ->> ABB: render(GameState)
        ABB -->> Player: Undo disabled, Resign disabled, New Game enabled
    end

    Note over GC, Clock: Each Frame — Clock Timeout Check
    GC ->> CC: update(delta)
    CC ->> Clock: tick(delta)
    CC ->> Clock: is_time_expired(active_color)
    Clock -->> CC: expired (bool)
    alt Time expired
        CC -->> GC: timeout = true
        GC ->> GState: status = TIMEOUT, winner = opponent_color
        GC ->> CC: stop_clock()
        CC ->> Clock: stop()
        GC -->> GS: game over
        GS ->> SB: render(GameState)
        SB ->> GState: get_result_message()
        GState -->> SB: "[Color] ran out of time. [Other color] wins!"
        SB -->> Player: display timeout result
        GS ->> ABB: render(GameState)
        ABB -->> Player: Only New Game available
    end
```

---

## Use Case to Diagram Traceability

| Use Case | Diagram | Primary Flow Shown |
|----------|---------|-------------------|
| UC-01: Launch Application | [Diagram 1](#1-application-launch-and-navigation-uc-01-uc-02-uc-11) | App launch, start menu display, exit |
| UC-02: View Credits | [Diagram 1](#1-application-launch-and-navigation-uc-01-uc-02-uc-11) | Credits navigation and return |
| UC-03: Select Time Control | [Diagram 2](#2-time-control-selection-and-game-initialization-uc-03-uc-04) | Preset and custom time selection |
| UC-04: Play Game | [Diagram 2](#2-time-control-selection-and-game-initialization-uc-03-uc-04) | Game initialization and board setup |
| UC-05: Move Piece | [Diagram 3](#3-move-piece-and-capture-uc-05-uc-06) | Full drag-and-drop flow with post-move checks |
| UC-06: Capture Piece | [Diagram 3](#3-move-piece-and-capture-uc-05-uc-06) | Capture as optional branch within move flow |
| UC-07a: Castling | [Diagram 4](#4-castling-uc-07a) | Castling preconditions and King/Rook execution |
| UC-07b: En Passant | [Diagram 5](#5-en-passant-uc-07b) | En passant validation and diagonal capture |
| UC-08: Promote Pawn | [Diagram 6](#6-pawn-promotion-uc-08) | Promotion popup, piece selection, replacement |
| UC-09: Undo Move | [Diagram 7](#7-undo-move-uc-09) | Full state reversal (board, clock, captures, flags) |
| UC-10: Resign | [Diagram 8](#8-resign-uc-10) | Resignation and game-over transition |
| UC-11: Start New Game | [Diagram 1](#1-application-launch-and-navigation-uc-01-uc-02-uc-11) | Navigation back to time select screen |
| Game End Conditions | [Diagram 9](#9-game-end-conditions) | Checkmate, stalemate, draw, timeout detection |
