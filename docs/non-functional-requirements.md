# Non-Functional Requirements

## NFR-01: Performance

- **NFR-01.1**: The system shall respond to user input (drag initiation, piece drop, button clicks) within 200 milliseconds.
- **NFR-01.2**: The application shall launch and display the start menu within 3 seconds.
- **NFR-01.3**: Move validation and board state updates shall complete within 100 milliseconds.
- **NFR-01.4**: The dragged piece shall track the mouse cursor at the application's frame rate with no perceptible lag.
- **NFR-01.5**: Player clocks shall update with at least 100ms precision and display with 1-second granularity (or 0.1-second when under 10 seconds).

## NFR-02: Usability

- **NFR-02.1**: The user interface shall be intuitive enough for a player familiar with chess rules to use without documentation.
- **NFR-02.2**: Chess pieces shall be clearly distinguishable by type and color.
- **NFR-02.3**: The board shall use a standard color scheme with alternating light and dark squares.
- **NFR-02.4**: Legal move highlights shall be clearly visible while dragging a piece.
- **NFR-02.5**: The current game state (turn, clocks, check status, captured pieces, point advantage) shall be visible at all times during a game.
- **NFR-02.6**: The board flip between turns shall be immediate and not disorienting.
- **NFR-02.7**: All menu screens (start menu, credits, time selection) shall be navigable with clear button labels. In this instance, clear is defined as:
    - **NFR-02.7.1**: A button containing text in legible font and color that states the buttons action


## NFR-03: Reliability

- **NFR-03.1**: The game logic shall correctly enforce all standard chess rules without exception.
- **NFR-03.2**: The application shall not crash or enter an invalid state during normal gameplay.
- **NFR-03.3**: The undo function shall restore the exact previous board state, including clock times, castling rights, and en passant eligibility.
- **NFR-03.4**: The clock shall never drift or miscount during a game.

## NFR-04: Maintainability

- **NFR-04.1**: The codebase shall follow a clear separation between game logic and user interface.
- **NFR-04.2**: The codebase shall follow PEP 8 style guidelines.
- **NFR-04.3**: All public modules and classes shall include docstrings.
- **NFR-04.4**: The project shall include unit tests for core game logic (move validation, check/checkmate detection, special moves, timer behavior).

## NFR-05: Portability

- **NFR-05.1**: The application shall run on Windows, macOS, and Linux.
- **NFR-05.2**: The application shall use cross-platform libraries only (Pygame for GUI).
- **NFR-05.3**: The application shall require Python 3.8 or later.

## NFR-06: Scalability

- **NFR-06.1**: The architecture shall allow for future addition of features such as AI opponents, online multiplayer, or game saving/loading without major refactoring.

## NFR-07: Accessibility

- **NFR-07.1**: Piece colors and board colors shall have sufficient contrast for readability.
- **NFR-07.2**: Text (clocks, move history, labels) shall be legible at the application's default window size.

## NFR-08: Dependencies

- **NFR-08.1**: The application shall minimize external dependencies.
- **NFR-08.2**: All dependencies shall be listed in a `requirements.txt` file.
- **NFR-08.3**: The GUI library shall be Pygame.
