# CIS-553-Chess

A two-player desktop chess application built in Python with Pygame. Supports drag-and-drop piece interaction, configurable time controls, full chess rule enforcement (including castling, en passant, pawn promotion), move history in algebraic notation, and undo/resign functionality.

## Documentation

Project documentation is located in the `docs/` directory:

- **functional-requirements.md** — Functional requirements (FR-01 through FR-16)
- **non-functional-requirements.md** — Non-functional requirements (performance, usability, maintainability, etc.)
- **use-case-model.md** — Use case descriptions (UC-01 through UC-11)
- **data-dictionary.md** — Data entities, attributes, and structures
- **ui-mockups.md** — Text-based wireframes for all screens
- **class-diagram.md** — Entity class diagram with relationships
- **boundary-classes.md** — Boundary (UI) class identification
- **control-classes.md** — Control (logic) class identification
- **dialog-map.md** — UI state machine with screen transitions

### Viewing Diagrams

Several documents (`class-diagram.md`, `dialog-map.md`, `control-classes.md`) contain [Mermaid](https://mermaid.js.org/) diagrams. To render them:

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
