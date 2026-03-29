from typing import Callable, Optional

import pygame

from src.screens.base_screen import BaseScreen
from src.components.button import Button
from src.components.promotion_popup import PromotionPopup
from src.entities.enums import Color, PieceType, GameStatus
from src.entities.drag_state import DragState
from src.controllers.game_controller import GameController
from src.controllers.input_controller import InputController
from src.constants import (
    COLOR_BACKGROUND,
    LIGHT_SQUARE,
    DARK_SQUARE,
    BOARD_BORDER,
    BOARD_BORDER_P,
    COLOR_TEXT,
    COLOR_HIGHLIGHT_ORIGIN,
    COLOR_PANEL,
    COLOR_BUTTON,
    FONT_NAME,
    FONT_SIZE_SMALL,
    FONT_SIZE_BODY,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# ── Piece rendering ────────────────────────────────────────────────────
# Placeholder assets: colored circles with a letter abbreviation.
# To swap in real PNGs later, replace _draw_piece() or load images into
# PIECE_IMAGES and blit them instead.

PIECES = {
    PieceType.KING: "K",
    PieceType.QUEEN: "Q",
    PieceType.ROOK: "R",
    PieceType.BISHOP: "B",
    PieceType.KNIGHT: "N",
    PieceType.PAWN: "P",
}

PIECE_WHITE = {
    PieceType.KING: pygame.image.load("assets/Pieces/KingWhite.png"),
    PieceType.QUEEN: pygame.image.load("assets/Pieces/QueenWhite.png"),
    PieceType.ROOK: pygame.image.load("assets/Pieces/RookWhite.png"),
    PieceType.BISHOP: pygame.image.load("assets/Pieces/BishopWhite.png"),
    PieceType.KNIGHT: pygame.image.load("assets/Pieces/KnightWhite.png"),
    PieceType.PAWN: pygame.image.load("assets/Pieces/PawnWhite.png")
}

PIECE_BLACK = {
    PieceType.KING: pygame.image.load("assets/Pieces/KingBlack.png"),
    PieceType.QUEEN: pygame.image.load("assets/Pieces/QueenBlack.png"),
    PieceType.ROOK: pygame.image.load("assets/Pieces/RookBlack.png"),
    PieceType.BISHOP: pygame.image.load("assets/Pieces/BishopBlack.png"),
    PieceType.KNIGHT: pygame.image.load("assets/Pieces/KnightBlack.png"),
    PieceType.PAWN: pygame.image.load("assets/Pieces/PawnBlack.png")
}

# Sort order for captured pieces display (highest value first)
PIECE_SORT_ORDER = {
    PieceType.QUEEN: 0,
    PieceType.ROOK: 1,
    PieceType.BISHOP: 2,
    PieceType.KNIGHT: 3,
    PieceType.PAWN: 4,
}

COLOR_WHITE_PIECE = (255, 255, 255)
COLOR_BLACK_PIECE = (30, 30, 30)
COLOR_WHITE_PIECE_TEXT = (30, 30, 30)
COLOR_BLACK_PIECE_TEXT = (220, 220, 220)

# Move history panel
PANEL_PADDING = 10
HISTORY_ROW_HEIGHT = 24

class GameScreen(BaseScreen):
    """Game screen with interactive drag-and-drop chess."""

    def __init__(
        self,
        surface: pygame.Surface,
        game_controller: GameController,
        on_back: Optional[Callable[[], None]] = None,
        on_new: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(surface)
        self._game_controller = game_controller
        self._on_back = on_back
        screen_w, screen_h = surface.get_size()

        # Board sizing: fit to ~75% of screen height, shifted left for side panel
        board_margin = 150
        self._square_size = (screen_h - board_margin * 2) // 8
        self._board_size = self._square_size * 8
        self._border_size = self._board_size + (BOARD_BORDER_P * 2)

        # Background
        self._scaled_back = pygame.transform.scale(COLOR_BACKGROUND.convert_alpha(), self.surface.get_size())
        
        # End Game Screen
        self._game_over_popup = pygame.Surface((screen_w - 200, 150), pygame.SRCALPHA)
        self._game_over_rect = pygame.Rect(0, 0, screen_w - 200, 125)
        self._game_over_pos = (100, screen_h-125)

        # Position board left of center to make room for history panel
        panel_width = 200
        total_width = self._board_size + 20 + panel_width
        left_offset = (screen_w - total_width) // 2
        self._board_x = left_offset - 175
        self._board_y = ((screen_h - (self._board_size + BOARD_BORDER_P)) // 2) - 50

        # Move history panel region (right of board)
        self._panel_x = self._board_x + self._board_size + 20
        self._panel_y = self._board_y
        self._panel_w = panel_width
        self._panel_h = self._board_size

        # Piece Collection Trays (3/4 size of board height)
        self._pc_tray = pygame.transform.scale(pygame.image.load("assets/PieceCollection.png"),(self._square_size*2, self._border_size * 0.75))

        # Captured pieces display regions
        self._captured_font_size = max(16, self._square_size // 4)

        # Fonts
        self._label_font = pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL)
        self._piece_font = pygame.font.Font(FONT_NAME, int(self._square_size * 0.45))
        self._status_font = pygame.font.Font(FONT_NAME, FONT_SIZE_BODY)
        self._history_font = pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL - 5)
        self._captured_font = pygame.font.Font(None, self._captured_font_size)
        self._advantage_font = pygame.font.Font(FONT_NAME, int(FONT_SIZE_BODY * 0.75))

        # Main Menu button (bottom right)
        self._back_button = Button(
            label="Main Menu",
            rect=pygame.Rect(
                self._panel_x + BOARD_BORDER_P + 530, 
                self._panel_y + self._panel_h + 125, 
                BUTTON_WIDTH - 35, 
                BUTTON_HEIGHT + 10),
            on_click=on_back,
            small_font=True
        )

        # New Game button (bottom right)
        self._new_game_button = Button(
            label="New Game",
            rect=pygame.Rect(
                screen_w - 600, 
                screen_h - 100, 
                BUTTON_WIDTH - 35, 
                BUTTON_HEIGHT + 10),
            on_click=on_new,
            small_font=True,
            enabled=False
        )    

        # Resign
        self._resign_button = Button(
            label="Resign",
            rect=pygame.Rect(
                self._panel_x + BOARD_BORDER_P + 300, 
                self._panel_y + self._panel_h + 125, 
                BUTTON_WIDTH - 40, 
                BUTTON_HEIGHT + 10),
            on_click=self._on_resign,
            small_font=True
        )

        # Undo button (below back button)
        self._undo_button = Button(
            label="Undo",
            rect=pygame.Rect(
                self._panel_x + BOARD_BORDER_P + 75, 
                self._panel_y + self._panel_h + 125, 
                BUTTON_WIDTH - 40, 
                BUTTON_HEIGHT + 10),
            on_click=self._on_undo,
            small_font=True
        )

        # Pre-render static board surface (squares + labels)
        self._board_surface = self._render_board()

        # Pre-render piece surfaces keyed by (PieceType, Color)
        self._piece_surfaces = self._render_pieces()

        # Promotion popup
        self._promotion_popup: Optional[PromotionPopup] = None

        # Move history scroll offset
        self._history_scroll = 0

        # Drag-and-drop state and input controller
        self._drag_state = DragState()
        self._input_controller = InputController(
            drag_state=self._drag_state,
            board_x=self._board_x,
            board_y=self._board_y,
            square_size=self._square_size,
            get_legal_moves_fn=self._game_controller.get_legal_moves,
            get_current_turn_fn=self._get_current_turn,
        )

    def _get_current_turn(self) -> Color:
        """Return the color whose turn it is."""
        return self._game_controller.game_state.board.current_turn

    def _render_board(self) -> pygame.Surface:
        """Draw the 8x8 board with rank/file labels onto a surface."""
        sq = self._square_size
        playable_surf = pygame.Surface((self._board_size, self._board_size))
        border_surf = pygame.Surface((self._border_size, self._border_size))
        border = pygame.transform.scale(BOARD_BORDER.convert_alpha(), (self._border_size, self._border_size))
        border_surf.blit(border, (0, 0))
        for row in range(8):
            for col in range(8):
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE.convert_alpha() if is_light else DARK_SQUARE.convert_alpha()
                playable_surf.blit(color, (col * sq,row * sq, sq, sq))

        border_surf.blit(playable_surf, (BOARD_BORDER_P,BOARD_BORDER_P))
        return border_surf

    def _render_pieces(self) -> dict:
        """Pre-render placeholder piece surfaces (circle + letter)."""
        sq = self._square_size
        surfaces = {}
        for piece_type in PieceType:
            for color in Color:
                piece = (
                    pygame.transform.scale(PIECE_WHITE[piece_type].convert_alpha(), (sq,sq))
                    if color == Color.WHITE
                    else pygame.transform.scale(PIECE_BLACK[piece_type].convert_alpha(), (sq,sq))
                )
                piece_surf = pygame.Surface((sq,sq), pygame.SRCALPHA)
                piece_surf.blit(piece, piece_surf.get_rect(center=(sq // 2, sq // 2)))
        
                surfaces[(piece_type, color)] = piece_surf

        return surfaces

    def _on_undo(self) -> None:
        """Callback when the Undo button is clicked."""
        self._game_controller.undo_last_move()

    def _on_resign(self) -> None:
        """Callback when Resign button is pressed."""
        self._game_controller.resign(self._game_controller.game_state.board.current_turn)
    
    def _on_promotion_select(self, piece_type: PieceType) -> None:
        """Callback when a promotion piece is selected."""
        self._game_controller.attempt_promotion(piece_type)
        self._promotion_popup = None

    def handle_event(self, event: pygame.event.Event) -> None:
        self._back_button.handle_event(event)
        self._resign_button.handle_event(event)
        self._undo_button.handle_event(event)
        self._new_game_button.handle_event(event)

        # Route events to promotion popup if active (modal)
        if self._promotion_popup is not None:
            self._promotion_popup.handle_event(event)
            return

        # Scroll move history with mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if (
                self._panel_x <= mx <= self._panel_x + self._panel_w
                and self._panel_y <= my <= self._panel_y + self._panel_h
            ):
                self._history_scroll -= event.y * HISTORY_ROW_HEIGHT * 2
                self._history_scroll = max(0, self._history_scroll)

        # No interaction during game over
        if self._game_controller.game_state.is_game_over():
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._input_controller.handle_mouse_down(
                event.pos, self._game_controller.game_state.board
            )
        elif event.type == pygame.MOUSEMOTION:
            self._input_controller.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            attempt = self._input_controller.handle_mouse_up(event.pos)
            if attempt is not None:
                result = self._game_controller.attempt_move(attempt)
                if result.is_promotion:
                    # Show promotion popup
                    color = self._game_controller.game_state.board.current_turn
                    pos = self._game_controller.game_state.pending_promotion
                    self._promotion_popup = PromotionPopup(
                        surface=self.surface,
                        square_size=self._square_size,
                        board_x=self._board_x,
                        board_y=self._board_y,
                        color=color,
                        position=pos,
                        on_select=self._on_promotion_select,
                    )

    def update(self, dt: float) -> None:
        self._game_controller.update(dt)

    def draw(self) -> None:
        self.surface.blit(self._scaled_back, (0,0))

        # Board background
        self.surface.blit(self._board_surface, (self._board_x, self._board_y))

        # Highlight origin square and legal moves if dragging
        if self._drag_state.is_dragging:
            self._draw_highlights()

        # Pieces from the board entity
        sq = self._square_size
        board = self._game_controller.game_state.board
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece is not None:
                    # Skip drawing the piece at the drag origin
                    if (
                        self._drag_state.is_dragging
                        and self._drag_state.origin
                        and self._drag_state.origin.row == row
                        and self._drag_state.origin.col == col
                    ):
                        continue
                    piece_surf = self._piece_surfaces[(piece.piece_type, piece.color)]
                    x = self._board_x + col * sq + BOARD_BORDER_P
                    y = self._board_y + row * sq + BOARD_BORDER_P
                    self.surface.blit(piece_surf, (x, y))

        # Draw dragged piece at cursor
        if (
            self._drag_state.is_dragging
            and self._drag_state.piece
            and self._drag_state.mouse_pos
        ):
            piece = self._drag_state.piece
            piece_surf = self._piece_surfaces[(piece.piece_type, piece.color)]
            mx, my = self._drag_state.mouse_pos
            self.surface.blit(piece_surf, (mx - sq // 2, my - sq // 2))

        # Captured pieces displays
        self._draw_captured_pieces()

        # Move history panel
        self._draw_move_history()        

        # Promotion popup (modal overlay)
        if self._promotion_popup is not None:
            self._promotion_popup.draw(self.surface)

        if not self._game_controller.game_state.is_game_over():
            # Buttons
            self._back_button.draw(self.surface)
            self._resign_button.draw(self.surface)

            # Undo button: enabled only when moves exist and game is active
            game_state = self._game_controller.game_state
            has_moves = len(game_state.board.move_history) > 0
            self._undo_button.enabled = has_moves and not game_state.is_game_over()
            self._undo_button.draw(self.surface)
            
            # Turn indicator / status text
            self._draw_status()
        else:
            pygame.draw.rect(self._game_over_popup, COLOR_PANEL, self._game_over_rect, border_radius=8)
            pygame.draw.rect(
                self._game_over_popup, (86, 49, 29), self._game_over_rect, width=10, border_radius=8
            )
            self.surface.blit(self._game_over_popup, self._game_over_pos)
            self._back_button.rect = pygame.Rect(
                                        self._new_game_button.rect.x + BUTTON_WIDTH - 20, 
                                        self._new_game_button.rect.y, 
                                        BUTTON_WIDTH - 35, 
                                        BUTTON_HEIGHT + 10
                                    )
            self._new_game_button.enabled = True
            self._new_game_button.draw(self.surface)
            self._back_button.draw(self.surface)            
            self._draw_status()
        

    def _draw_highlights(self) -> None:
        """Draw highlights on the origin square and legal move destinations."""
        sq = self._square_size

        # Highlight origin square with blue tint
        if self._drag_state.origin:
            origin_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)
            origin_surf.fill(COLOR_HIGHLIGHT_ORIGIN)
            ox = self._board_x + self._drag_state.origin.col * sq + BOARD_BORDER_P
            oy = self._board_y + self._drag_state.origin.row * sq + BOARD_BORDER_P
            self.surface.blit(origin_surf, (ox, oy))

        # Draw legal move indicators
        board = self._game_controller.game_state.board
        for move_pos in self._drag_state.legal_moves:
            cx = self._board_x + move_pos.col * sq + sq // 2 + BOARD_BORDER_P
            cy = self._board_y + move_pos.row * sq + sq // 2 + BOARD_BORDER_P

            target = board.get_piece(move_pos)
            if target is not None:
                # Capture highlight: semi-transparent ring
                ring_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)
                pygame.draw.circle(
                    ring_surf,
                    (0, 0, 0, 60),
                    (sq // 2, sq // 2),
                    sq // 2 - 2,
                    4,
                )
                self.surface.blit(
                    ring_surf,
                    (
                        self._board_x + move_pos.col * sq + BOARD_BORDER_P, 
                        self._board_y + move_pos.row * sq + BOARD_BORDER_P,
                    ),
                )
            else:
                # Normal move: small dot
                dot_surf = pygame.Surface((sq, sq), pygame.SRCALPHA)
                pygame.draw.circle(dot_surf, (0, 0, 0, 60), (sq // 2, sq // 2), sq // 6)
                self.surface.blit(
                    dot_surf,
                    (
                        self._board_x + move_pos.col * sq + BOARD_BORDER_P,
                        self._board_y + move_pos.row * sq + BOARD_BORDER_P,
                    ),
                )

    def _draw_captured_pieces(self) -> None:
        """Draw captured pieces for both players above and below the board."""
        game_state = self._game_controller.game_state
        captured = game_state.captured_pieces
        advantage = captured.get_point_advantage()

        # Draw collection tray
        # White tray
        self.surface.blit(self._pc_tray.convert_alpha(), (self._board_x - 200, self._board_y + 200))
        # Black tray
        self.surface.blit(self._pc_tray.convert_alpha(), (self._board_x + 5 + self._border_size, self._board_y + 200))

        # Pieces White has captured from Black
        self._draw_captured_row(
            captured.white_captured,
            Color.BLACK,
            self._board_x - 150,
            self._board_y + 135,
            advantage if advantage > 0 else 0,
        )

        # Pieces Black has captured from White
        self._draw_captured_row(
            captured.black_captured,
            Color.WHITE,
            self._board_x + self._border_size + 50,
            self._board_y + 135,
            -advantage if advantage < 0 else 0,
        )

    def _draw_captured_row(
        self,
        pieces: list,
        captured_color: Color,
        x: int,
        y: int,
        advantage: int,
    ) -> None:
        """Draw a row of captured piece symbols and point advantage."""
        if not pieces:
            return

        # Sort by piece value (highest first)
        sorted_pieces = sorted(
            pieces, key=lambda p: PIECE_SORT_ORDER.get(p.piece_type, 5)
        )

        # get x and y of piece if more than 8 wrap around,

        # Render each captured piece as a letter
        spacing = self._square_size - 5
        n_pieces = 0
        row = 0
        for piece in sorted_pieces:
            if captured_color == Color.BLACK:
                x_piece = self._board_x - 180 + (row * spacing - 10)
                y_piece = self._board_y + 225 + (spacing * n_pieces)
                piece = pygame.transform.scale(PIECE_BLACK.get(piece.piece_type, "?").convert_alpha(), (self._square_size - 20, self._square_size - 20))
            else:
                x_piece = self._board_x + 20 + self._border_size + (row * spacing - 10)
                y_piece = self._board_y + 225 + (spacing * n_pieces)
                piece = pygame.transform.scale(PIECE_WHITE.get(piece.piece_type, "?").convert_alpha(), (self._square_size - 20, self._square_size - 20))
            self.surface.blit(piece, (x_piece, y_piece))
            n_pieces += 1
            if n_pieces >= 7:
                n_pieces = 0
                row = 1
                

        # Point advantage
        if advantage > 0:
            adv_text = f"+{advantage}"
            adv_surf = self._advantage_font.render(adv_text, True, (255,255,255) if captured_color == Color.BLACK else (0,0,0))
            self.surface.blit(adv_surf, (x,y))

    def _draw_move_history(self) -> None:
        """Draw the move history panel to the right of the board."""
        px = self._panel_x + BOARD_BORDER_P + 375
        py = self._panel_y
        pw = self._panel_w + 150
        ph = self._panel_h

        # Panel background
        panel_rect = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(self.surface, COLOR_PANEL, panel_rect, border_radius=8)
        pygame.draw.rect(
            self.surface, (86, 49, 29), panel_rect, width=3, border_radius=8
        )

        # Header
        header_surf = self._history_font.render("Move History", True, COLOR_TEXT)
        self.surface.blit(header_surf, (px + PANEL_PADDING, py + PANEL_PADDING))

        # Build move pairs from move_history
        moves = self._game_controller.game_state.board.move_history
        move_pairs = []
        for i in range(0, len(moves), 2):
            move_num = i // 2 + 1
            white_move = moves[i].notation if i < len(moves) else ""
            black_move = moves[i + 1].notation if i + 1 < len(moves) else ""
            move_pairs.append((move_num, white_move, black_move))

        if not move_pairs:
            empty_surf = self._history_font.render("No moves yet", True, COLOR_TEXT)
            self.surface.blit(empty_surf, (px + PANEL_PADDING, py + PANEL_PADDING + 30))
            return

        # Clipping region for scrollable content
        content_y = py + PANEL_PADDING + 28
        content_h = ph - PANEL_PADDING * 2 - 28
        clip_rect = pygame.Rect(px, content_y, pw, content_h)

        # Auto-scroll to bottom
        total_height = len(move_pairs) * HISTORY_ROW_HEIGHT
        max_scroll = max(0, total_height - content_h)
        self._history_scroll = min(self._history_scroll, max_scroll)
        # Auto-scroll to latest move
        if total_height > content_h:
            self._history_scroll = max_scroll

        # Render move rows
        prev_clip = self.surface.get_clip()
        self.surface.set_clip(clip_rect)

        col_num_x = px + PANEL_PADDING
        col_white_x = px + PANEL_PADDING + 36
        col_black_x = px + PANEL_PADDING + 36 + (pw - 36 - PANEL_PADDING * 2) // 2

        for idx, (num, white, black) in enumerate(move_pairs):
            row_y = content_y + idx * HISTORY_ROW_HEIGHT - self._history_scroll

            if row_y + HISTORY_ROW_HEIGHT < content_y or row_y > content_y + content_h:
                continue

            # Alternate row background
            if idx % 2 == 0:
                row_bg = pygame.Rect(px + 2, row_y, pw - 4, HISTORY_ROW_HEIGHT)
                bg_surf = pygame.Surface((row_bg.width, row_bg.height), pygame.SRCALPHA)
                bg_surf.fill((255, 255, 255, 10))
                self.surface.blit(bg_surf, row_bg.topleft)

            # Move number
            num_surf = self._history_font.render(f"{num}.", True, COLOR_TEXT)
            self.surface.blit(num_surf, (col_num_x, row_y + 2))

            # White's move
            white_surf = self._history_font.render(white, True, COLOR_TEXT)
            self.surface.blit(white_surf, (col_white_x + 7, row_y + 2))

            # Black's move
            if black:
                black_surf = self._history_font.render(black, True, COLOR_TEXT)
                self.surface.blit(black_surf, (col_black_x + 7, row_y + 2))

        self.surface.set_clip(prev_clip)

    def _draw_status(self) -> None:
        """Draw turn indicator and game status text below the board."""
        game_state = self._game_controller.game_state
        status_x = self._board_x + self._board_size // 2
        status_y = self._board_y + self._board_size + 80 + BOARD_BORDER_P

        if game_state.is_game_over():
            # Change status location
            status_y = self._board_y + self._board_size + 70 + BOARD_BORDER_P
            status_x = self._board_x + self._board_size // 2 - 100
            text = game_state.get_result_message()
        elif game_state.status == GameStatus.CHECK:
            turn_name = game_state.board.current_turn.name.capitalize()
            text = f"{turn_name}'s turn - CHECK!"
        else:
            turn_name = game_state.board.current_turn.name.capitalize()
            text = f"{turn_name}'s turn"
        
        status_surf = self._status_font.render(text, True, COLOR_TEXT)
        status_rect = status_surf.get_rect(
            centerx=(status_x) + BOARD_BORDER_P, top=status_y
        )
        
        self.surface.blit(status_surf, status_rect)
