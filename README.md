# CIS-553-Chess

A two-player desktop chess application built in Python with Pygame. Supports drag-and-drop piece interaction, configurable time controls, full chess rule enforcement (including castling, en passant, pawn promotion), move history in algebraic notation, and undo/resign functionality.

## Features

- **Drag-and-drop** piece movement with legal move highlighting
- **All standard piece rules** — pawn, rook, bishop, queen, knight, king
- **Special moves** — castling (kingside/queenside), en passant, pawn promotion with selection popup
- **Check, checkmate, and stalemate** detection
- **Draw detection** — insufficient material, threefold repetition, fifty-move rule
- **Move history** in standard algebraic notation (e.g., Nf3, O-O, exd5, e8=Q)
- **Undo** — revert any move, including special moves and captures
- **Time control presets** — Bullet, Blitz, Rapid, Classic, No Time, or custom
- **Resign** functionality

## Documentation

Project documentation is located in the `docs/` directory:

- **system-architecture.md** — High-level architecture, layers, component diagram, design decisions
- **application-skeleton.md** — File structure, module descriptions, control flow traces
- **test-cases.md** — Test case catalog, requirement traceability, and latest test results
- **functional-requirements.md** — Functional requirements (FR-01 through FR-16)
- **non-functional-requirements.md** — Non-functional requirements (performance, usability, maintainability, etc.)
- **use-case-model.md** — Use case descriptions (UC-01 through UC-11)
- **data-dictionary.md** — Data entities, attributes, and structures
- **ui-mockups.md** — Text-based wireframes for all screens
- **class-diagram.md** — Entity class diagram with relationships
- **boundary-classes.md** — Boundary (UI) class identification
- **control-classes.md** — Control (logic) class identification
- **sequence-diagrams.md** — UML sequence diagrams for all use cases
- **dialog-map.md** — UI state machine with screen transitions

### Viewing Diagrams

Several documents (`class-diagram.md`, `dialog-map.md`, `control-classes.md`, `sequence-diagrams.md`) contain [Mermaid](https://mermaid.js.org/) diagrams. To render them:

- **GitHub**: Mermaid renders automatically in markdown previews.
- **VS Code**: Install the [Mermaid Extension](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart).

## Getting Started

### Prerequisites

- Python 3.8 or later

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd CIS-553-Chess
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python3 main.py
```

Press **ESC** to exit fullscreen.

## Testing

This project uses [pytest](https://docs.pytest.org/) for unit testing. Tests are located in the `tests/` directory.

### Running Tests

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Run a specific test file:

```bash
python -m pytest tests/test_castling.py -v
```

Run tests matching a keyword:

```bash
python -m pytest tests/ -k "en_passant" -v
```

## Code Formatting

This project uses [Black](https://black.readthedocs.io/) for consistent code formatting. Black is included in `requirements.txt` and configured in `pyproject.toml`.

Format all files before committing:

```bash
black src/ tests/
```

Check formatting without modifying files:

```bash
black --check src/ tests/
```