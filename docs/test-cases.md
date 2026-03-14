# Test Cases and Testing Results

This document catalogs all unit tests, describes the testing approach, and records the latest test results.

See also: [Functional Requirements](functional-requirements.md) | [Non-Functional Requirements](non-functional-requirements.md) | [System Architecture](system-architecture.md)

---

## Testing Framework

- **Framework**: [pytest](https://docs.pytest.org/) 9.0+
- **Configuration**: `pyproject.toml` — `testpaths = ["tests"]`
- **Shared fixtures**: `tests/conftest.py`

### Running Tests

```bash
# Full suite
python -m pytest tests/ -v

# Single file
python -m pytest tests/test_castling.py -v

# By keyword
python -m pytest tests/ -k "en_passant" -v
```

---

## Test Fixtures (`conftest.py`)

| Fixture | Returns | Purpose |
|---------|---------|---------|
| `empty_board` | `Board()` | Empty 8x8 board with no pieces |
| `standard_board` | `Board()` with `initialize_standard()` | Standard starting position (32 pieces) |
| `validator` | `MoveValidator()` | Stateless move legality checker |
| `draw_detector` | `DrawDetector()` | Stateless draw condition detector |

**Helper function**: `place_piece(board, algebraic, piece_type, color, has_moved=False)` — places a piece at an algebraic position (e.g., `"e4"`) and returns `(Position, Piece)`.

---

## Test Cases by File

### 1. Pawn Movement (`test_pawn_moves.py`) — 16 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_white_pawn_forward_one` | FR-07.1 | White pawn moves one square forward |
| 2 | `test_black_pawn_forward_one` | FR-07.1 | Black pawn moves one square forward (opposite direction) |
| 3 | `test_white_pawn_double_from_start` | FR-07.1 | White pawn moves two squares from starting rank |
| 4 | `test_black_pawn_double_from_start` | FR-07.1 | Black pawn moves two squares from starting rank |
| 5 | `test_white_pawn_blocked_by_piece` | FR-07.1 | Pawn cannot move forward when square is occupied |
| 6 | `test_white_pawn_double_blocked_on_first_square` | FR-07.1 | Double move blocked when first square is occupied |
| 7 | `test_white_pawn_double_blocked_on_second_square` | FR-07.1 | Double move blocked when second square is occupied |
| 8 | `test_white_pawn_captures_diagonally` | FR-08 | Pawn captures enemy piece diagonally |
| 9 | `test_white_pawn_cannot_capture_own_piece` | FR-07.3 | Pawn cannot capture same-color piece |
| 10 | `test_black_pawn_captures_diagonally` | FR-08 | Black pawn captures diagonally in correct direction |
| 11 | `test_white_en_passant_capture` | FR-09.2 | White pawn en passant after black double push |
| 12 | `test_black_en_passant_capture` | FR-09.2 | Black pawn en passant after white double push |
| 13 | `test_en_passant_not_available_without_double_push` | FR-09.2 | No en passant if last move was not a double push |
| 14 | `test_en_passant_not_available_if_not_adjacent` | FR-09.2 | No en passant if pawns are not adjacent |
| 15 | `test_white_pawn_can_reach_promotion_rank` | FR-09.3 | White pawn on 7th rank has legal move to 8th |
| 16 | `test_black_pawn_can_reach_promotion_rank` | FR-09.3 | Black pawn on 2nd rank has legal move to 1st |

---

### 2. Rook Movement (`test_rook_moves.py`) — 9 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_rook_horizontal_right` | FR-07.2 | Rook slides right along rank |
| 2 | `test_rook_horizontal_left` | FR-07.2 | Rook slides left along rank |
| 3 | `test_rook_vertical_up` | FR-07.2 | Rook slides up along file |
| 4 | `test_rook_vertical_down` | FR-07.2 | Rook slides down along file |
| 5 | `test_rook_total_moves_open_board` | FR-07.2 | Rook has 14 moves on an open board |
| 6 | `test_rook_blocked_by_own_piece` | FR-07.3 | Rook stops before own piece |
| 7 | `test_rook_cannot_jump_over_pieces` | FR-07.3 | Rook cannot jump over blocking pieces |
| 8 | `test_rook_captures_enemy_and_stops` | FR-08 | Rook captures enemy and does not continue past |
| 9 | `test_rook_no_diagonal_moves` | FR-07.2 | Rook has no diagonal movement |

---

### 3. Bishop Movement (`test_bishop_moves.py`) — 9 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_bishop_northeast` | FR-07.3 | Bishop slides along NE diagonal |
| 2 | `test_bishop_northwest` | FR-07.3 | Bishop slides along NW diagonal |
| 3 | `test_bishop_southeast` | FR-07.3 | Bishop slides along SE diagonal |
| 4 | `test_bishop_southwest` | FR-07.3 | Bishop slides along SW diagonal |
| 5 | `test_bishop_total_moves_open_board` | FR-07.3 | Bishop has 13 moves from center on open board |
| 6 | `test_bishop_blocked_by_own_piece` | FR-07.3 | Bishop stops before own piece |
| 7 | `test_bishop_cannot_jump_over_pieces` | FR-07.3 | Bishop cannot jump over blocking pieces |
| 8 | `test_bishop_captures_enemy_and_stops` | FR-08 | Bishop captures enemy piece on diagonal |
| 9 | `test_bishop_no_horizontal_or_vertical_moves` | FR-07.3 | Bishop has no horizontal or vertical movement |

---

### 4. Queen Movement (`test_queen_moves.py`) — 8 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_queen_horizontal_moves` | FR-07.5 | Queen slides horizontally |
| 2 | `test_queen_vertical_moves` | FR-07.5 | Queen slides vertically |
| 3 | `test_queen_diagonal_moves` | FR-07.5 | Queen slides diagonally |
| 4 | `test_queen_total_moves_open_board` | FR-07.5 | Queen has 27 moves from center on open board |
| 5 | `test_queen_blocked_by_own_piece_horizontal` | FR-07.3 | Queen stops before own piece on rank |
| 6 | `test_queen_blocked_by_own_piece_diagonal` | FR-07.3 | Queen stops before own piece on diagonal |
| 7 | `test_queen_captures_enemy_horizontal` | FR-08 | Queen captures enemy piece horizontally |
| 8 | `test_queen_captures_enemy_diagonal` | FR-08 | Queen captures enemy piece diagonally |

---

### 5. Knight Movement (`test_knight_moves.py`) — 10 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_knight_all_eight_moves_from_center` | FR-07.4 | All 8 L-shaped destinations from center |
| 2 | `test_knight_count_from_center` | FR-07.4 | Knight has exactly 8 moves from center |
| 3 | `test_knight_jumps_over_own_pieces` | FR-07.4 | Knight jumps over own pieces |
| 4 | `test_knight_jumps_over_enemy_pieces` | FR-07.4 | Knight jumps over enemy pieces |
| 5 | `test_knight_cannot_land_on_own_piece` | FR-07.3 | Knight cannot land on same-color piece |
| 6 | `test_knight_captures_enemy_piece` | FR-08 | Knight captures enemy at destination |
| 7 | `test_knight_captures_multiple_enemies` | FR-08 | Knight can capture any of multiple enemies |
| 8 | `test_knight_from_corner_a1` | FR-07.4 | Knight has 2 moves from corner a1 |
| 9 | `test_knight_from_corner_h8` | FR-07.4 | Knight has 2 moves from corner h8 |
| 10 | `test_knight_from_edge_a4` | FR-07.4 | Knight has 4 moves from edge a4 |

---

### 6. King Movement (`test_king_moves.py`) — 6 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_king_moves_all_directions_from_center` | FR-07.6 | King has 8 moves from center |
| 2 | `test_king_moves_from_corner` | FR-07.6 | King has 3 moves from corner |
| 3 | `test_king_blocked_by_own_pieces` | FR-07.3 | King has 0 moves when fully surrounded by own pieces |
| 4 | `test_king_can_capture_enemy` | FR-08 | King captures adjacent enemy piece |
| 5 | `test_king_cannot_move_into_check` | FR-10.2 | King cannot move to square attacked by enemy rook |
| 6 | `test_king_cannot_move_adjacent_to_enemy_king` | FR-10.2 | Kings cannot occupy adjacent squares |

---

### 7. Castling (`test_castling.py`) — 19 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_kingside_in_legal_moves` (white) | FR-09.1 | White king can castle kingside when conditions met |
| 2 | `test_queenside_in_legal_moves` (white) | FR-09.1 | White king can castle queenside when conditions met |
| 3 | `test_kingside_in_legal_moves` (black) | FR-09.1 | Black king can castle kingside |
| 4 | `test_queenside_in_legal_moves` (black) | FR-09.1 | Black king can castle queenside |
| 5 | `test_king_has_moved` | FR-09.1.1 | No castling if king has moved |
| 6 | `test_rook_has_moved` | FR-09.1.2 | No castling if rook has moved |
| 7 | `test_piece_between_king_and_rook_kingside` | FR-09.1.3 | No castling if piece blocks kingside path |
| 8 | `test_piece_between_king_and_rook_queenside` | FR-09.1.3 | No castling if piece blocks queenside path |
| 9 | `test_king_in_check` | FR-09.1.4 | No castling while king is in check |
| 10 | `test_king_passes_through_attacked_square` | FR-09.1.5 | No castling if king passes through attacked square |
| 11 | `test_king_lands_on_attacked_square` | FR-09.1.6 | No castling if destination is attacked |
| 12 | `test_kingside_execution` (white) | FR-09.1 | King at g1, rook at f1 after kingside castle |
| 13 | `test_queenside_execution` (white) | FR-09.1 | King at c1, rook at d1 after queenside castle |
| 14 | `test_black_kingside_execution` | FR-09.1 | King at g8, rook at f8 after black kingside castle |
| 15 | `test_black_queenside_execution` | FR-09.1 | King at c8, rook at d8 after black queenside castle |
| 16 | `test_undo_kingside` | FR-15.1 | Undo restores king and rook to original squares |
| 17 | `test_undo_queenside` | FR-15.1 | Undo restores king and rook for queenside |
| 18 | `test_kingside_notation` | FR-14.1 | Notation is "O-O" for kingside castling |
| 19 | `test_queenside_notation` | FR-14.1 | Notation is "O-O-O" for queenside castling |

---

### 8. En Passant (`test_en_passant.py`) — 10 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_valid_en_passant_left` | FR-09.2 | White captures en passant to the left |
| 2 | `test_valid_en_passant_right` | FR-09.2 | White captures en passant to the right |
| 3 | `test_valid_en_passant` (black) | FR-09.2 | Black captures en passant |
| 4 | `test_last_move_not_double_push` | FR-09.2 | No en passant if last move was a single push |
| 5 | `test_pawn_not_on_correct_rank` | FR-09.2 | No en passant if pawn not on 5th rank |
| 6 | `test_pawn_not_adjacent` | FR-09.2 | No en passant if pawn not adjacent to opponent |
| 7 | `test_captured_pawn_removed` (white) | FR-09.2 | Captured pawn removed from board after execution |
| 8 | `test_black_en_passant_execution` | FR-09.2 | Black en passant removes white pawn |
| 9 | `test_undo_restores_both_pawns` | FR-15.1 | Undo restores both pawns to original positions |
| 10 | `test_undo_black_en_passant` | FR-15.1 | Undo restores black en passant correctly |

---

### 9. Pawn Promotion (`test_promotion.py`) — 16 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_move_returns_is_promotion` | FR-09.3 | `MoveResult.is_promotion` is True when pawn reaches back rank |
| 2 | `test_pending_promotion_set` | FR-09.3 | `GameState.pending_promotion` is set to the promotion square |
| 3 | `test_promote_to_queen` | FR-09.3 | Pawn replaced with queen after `attempt_promotion(QUEEN)` |
| 4 | `test_pending_promotion_cleared` | FR-09.3 | `pending_promotion` is None after promotion completes |
| 5 | `test_turn_switches_after_promotion` | FR-09.3 | Turn switches to opponent after promotion |
| 6–9 | `test_promote_to_each_piece` (x4) | FR-09.3 | Promotion to Queen, Rook, Bishop, Knight each works |
| 10 | `test_capture_promotion` | FR-09.3, FR-08 | Pawn captures and promotes simultaneously |
| 11 | `test_captured_piece_tracked` | FR-08 | Captured piece added to CapturedPieces during promotion |
| 12 | `test_queen_promotion_notation` | FR-14.1 | Notation includes "=Q" |
| 13 | `test_rook_promotion_notation` | FR-14.1 | Notation includes "=R" |
| 14 | `test_bishop_promotion_notation` | FR-14.1 | Notation includes "=B" |
| 15 | `test_knight_promotion_notation` | FR-14.1 | Notation includes "=N" |
| 16 | `test_capture_promotion_notation` | FR-14.1 | Notation includes capture + promotion (e.g., "exd8=Q") |

---

### 10. Check Detection (`test_check_detection.py`) — 12 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_king_in_check_from_rook` | FR-10.1 | Rook gives check along file |
| 2 | `test_king_in_check_from_bishop` | FR-10.1 | Bishop gives check along diagonal |
| 3 | `test_king_in_check_from_knight` | FR-10.1 | Knight gives check from L-shape |
| 4 | `test_king_in_check_from_pawn` | FR-10.1 | Pawn gives check diagonally |
| 5 | `test_king_not_in_check` | FR-10.1 | King is safe (no check) |
| 6 | `test_scholars_mate` | FR-10.3 | Scholar's mate detected as checkmate |
| 7 | `test_back_rank_mate` | FR-10.3 | Back rank mate detected as checkmate |
| 8 | `test_not_checkmate_when_can_escape` | FR-10.3 | Check with escape is not checkmate |
| 9 | `test_stalemate_king_cornered` | FR-10.4 | Cornered king with no legal moves is stalemate |
| 10 | `test_not_stalemate_when_in_check` | FR-10.4 | Check with no moves is checkmate, not stalemate |
| 11 | `test_king_cannot_move_into_check` | FR-10.2 | Attacked squares excluded from king's legal moves |
| 12 | `test_must_escape_check` | FR-10.2 | Only check-resolving moves are legal when in check |

---

### 11. Draw Detection (`test_draw_detection.py`) — 16 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_king_vs_king` | FR-11.2 | K vs K is insufficient material |
| 2 | `test_king_bishop_vs_king` | FR-11.2 | K+B vs K is insufficient material |
| 3 | `test_king_knight_vs_king` | FR-11.2 | K+N vs K is insufficient material |
| 4 | `test_king_bishop_vs_king_bishop_same_color_squares` | FR-11.2 | K+B vs K+B (same color bishops) is insufficient |
| 5 | `test_king_bishop_vs_king_bishop_different_color_squares` | FR-11.2 | K+B vs K+B (different color bishops) is NOT insufficient |
| 6 | `test_king_queen_vs_king_not_insufficient` | FR-11.2 | K+Q vs K is NOT insufficient material |
| 7 | `test_threefold_repetition_detected` | FR-11.3 | Same position hash 3 times triggers draw |
| 8 | `test_not_threefold_with_two_occurrences` | FR-11.3 | Two occurrences does not trigger draw |
| 9 | `test_empty_position_history` | FR-11.3 | Empty history does not trigger draw |
| 10 | `test_fifty_move_rule_triggered` | FR-11.4 | `halfmove_clock == 100` triggers draw |
| 11 | `test_fifty_move_rule_not_triggered` | FR-11.4 | `halfmove_clock == 99` does not trigger draw |
| 12 | `test_fifty_move_rule_above_100` | FR-11.4 | `halfmove_clock > 100` still triggers draw |
| 13 | `test_returns_insufficient_material` | FR-11 | `check_draw_conditions` returns `DRAW_INSUFFICIENT_MATERIAL` |
| 14 | `test_returns_fifty_move` | FR-11 | `check_draw_conditions` returns `DRAW_FIFTY_MOVE` |
| 15 | `test_returns_threefold_repetition` | FR-11 | `check_draw_conditions` returns `DRAW_THREEFOLD_REPETITION` |
| 16 | `test_returns_none_when_no_draw` | FR-11 | `check_draw_conditions` returns `None` when no draw |

---

### 12. Algebraic Notation (`test_notation.py`) — 10 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_normal_pawn_move` | FR-14.1 | Pawn move notation: "e4" |
| 2 | `test_pawn_capture` | FR-14.1 | Pawn capture notation: "exd5" |
| 3 | `test_knight_move` | FR-14.1 | Knight move notation: "Nf3" |
| 4 | `test_bishop_capture` | FR-14.1 | Bishop capture notation: "Bxe5" |
| 5 | `test_kingside_castling` | FR-14.1 | Castling notation: "O-O" |
| 6 | `test_queenside_castling` | FR-14.1 | Castling notation: "O-O-O" |
| 7 | `test_promotion_to_queen` | FR-14.1 | Promotion notation: "e8=Q" |
| 8 | `test_promotion_with_capture` | FR-14.1 | Capture+promotion notation: "exd8=Q" |
| 9 | `test_disambiguation_by_file` | FR-14.1 | File disambiguation: "Rad1" |
| 10 | `test_disambiguation_by_rank` | FR-14.1 | Rank disambiguation: "R1a4" |

---

### 13. Board Operations (`test_board.py`) — 10 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_execute_move_sets_has_moved` | FR-07 | `piece.has_moved` set to True after execution |
| 2 | `test_execute_castling_moves_king_and_rook` | FR-09.1 | Both king and rook move during castling |
| 3 | `test_execute_en_passant_removes_captured_pawn` | FR-09.2 | Captured pawn removed from board |
| 4 | `test_execute_promotion_replaces_pawn` | FR-09.3 | Pawn replaced with promoted piece |
| 5 | `test_undo_move_reverts_has_moved` | FR-15.1 | `has_moved` reverted to pre-move value |
| 6 | `test_undo_castling_restores_both_pieces` | FR-15.1 | King and rook return to original squares |
| 7 | `test_undo_en_passant_restores_captured_pawn` | FR-15.1 | Captured pawn restored to correct position |
| 8 | `test_clone_produces_independent_copy` | NFR-03 | Modifying clone does not affect original |
| 9 | `test_hash_changes_when_piece_moves` | FR-11.3 | Position hash changes after a move |
| 10 | `test_hash_includes_castling_rights` | FR-11.3 | Hash differs when castling rights differ |

---

### 14. Undo Move (`test_undo.py`) — 9 tests

| # | Test | FR | Description |
|---|------|----|-------------|
| 1 | `test_undo_returns_true_on_success` | FR-15.1 | `undo_last_move()` returns True when moves exist |
| 2 | `test_undo_returns_false_no_moves` | FR-15.1 | `undo_last_move()` returns False with no history |
| 3 | `test_undo_restores_piece_to_origin` | FR-15.1 | Piece returns to starting square, destination empty |
| 4 | `test_undo_switches_turn_back` | FR-15.1 | Turn reverts to the previous player |
| 5 | `test_undo_removes_move_from_history` | FR-15.1 | Move removed from `move_history` |
| 6 | `test_undo_multiple_moves` | FR-15.1 | Three sequential undos all work correctly |
| 7 | `test_undo_restores_captured_piece` | FR-15.1 | Captured piece returns to board and CapturedPieces updated |
| 8 | `test_undo_clears_game_over` | FR-15.1 | Undoing a check/checkmate restores ACTIVE status |
| 9 | `test_undo_sets_status_active` | FR-15.1 | Status is ACTIVE after undoing a normal move |

---

## Requirement Traceability Matrix

| Functional Requirement | Test File(s) | Test Count |
|------------------------|-------------|------------|
| FR-07: Piece Movement Rules | `test_pawn_moves`, `test_rook_moves`, `test_bishop_moves`, `test_queen_moves`, `test_knight_moves`, `test_king_moves` | 58 |
| FR-08: Capturing | `test_pawn_moves`, `test_rook_moves`, `test_bishop_moves`, `test_queen_moves`, `test_knight_moves`, `test_king_moves`, `test_promotion` | 14 |
| FR-09.1: Castling | `test_castling` | 19 |
| FR-09.2: En Passant | `test_pawn_moves`, `test_en_passant` | 14 |
| FR-09.3: Pawn Promotion | `test_pawn_moves`, `test_promotion` | 18 |
| FR-10: Check, Checkmate, Stalemate | `test_check_detection`, `test_king_moves` | 18 |
| FR-11: Draw Conditions | `test_draw_detection` | 16 |
| FR-14: Move History (Notation) | `test_notation`, `test_castling`, `test_promotion` | 15 |
| FR-15.1: Undo Move | `test_undo`, `test_castling`, `test_en_passant`, `test_board` | 16 |

---

## Latest Test Results

**Date**: 2026-03-14

**Environment**:
- Python 3.10.12
- pytest 9.0.2
- Platform: Linux (WSL2)

**Result**: **160 passed** in **0.14s**

```
tests/test_bishop_moves.py    9 passed
tests/test_board.py           10 passed
tests/test_castling.py        19 passed
tests/test_check_detection.py 12 passed
tests/test_draw_detection.py  16 passed
tests/test_en_passant.py      10 passed
tests/test_king_moves.py       6 passed
tests/test_knight_moves.py    10 passed
tests/test_notation.py        10 passed
tests/test_pawn_moves.py      16 passed
tests/test_promotion.py       16 passed
tests/test_queen_moves.py      8 passed
tests/test_rook_moves.py       9 passed
tests/test_undo.py             9 passed
─────────────────────────────────────────
TOTAL                        160 passed, 0 failed
```

All 160 tests pass with zero failures or warnings.
