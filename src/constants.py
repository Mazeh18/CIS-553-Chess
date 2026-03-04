import pygame

# ── Window ──────────────────────────────────────────────────────────────
WINDOW_TITLE = "Chess"
FPS = 60

# ── Colors (from docs/ui-mockups.md) ───────────────────────────────────
COLOR_BACKGROUND = (49, 46, 43)  # #312E2B
COLOR_PANEL = (60, 58, 55)  # #3C3A37
COLOR_TEXT = (255, 255, 255)  # #FFFFFF
COLOR_TEXT_DIM = (180, 180, 180)
COLOR_BUTTON = (90, 87, 82)  # neutral gray
COLOR_BUTTON_HOVER = (110, 107, 100)
COLOR_BUTTON_DISABLED = (65, 62, 58)
COLOR_BUTTON_BORDER = (140, 135, 125)
COLOR_BUTTON_TEXT = (255, 255, 255)

# Board colors
COLOR_LIGHT_SQUARE = (240, 217, 181)  # #F0D9B5
COLOR_DARK_SQUARE = (181, 136, 99)  # #B58863
COLOR_LABEL = (160, 152, 140)  # rank/file labels on the board

# ── Typography ─────────────────────────────────────────────────────────
FONT_NAME = None  # Pygame default; swap to a .ttf path for custom fonts

FONT_SIZE_TITLE = 72
FONT_SIZE_HEADING = 48
FONT_SIZE_BUTTON = 32
FONT_SIZE_BODY = 24
FONT_SIZE_SMALL = 18

# Board highlights (drag-and-drop)
COLOR_HIGHLIGHT_ORIGIN = (70, 130, 180, 100)  # blue tint on origin square

# ── Button Defaults ────────────────────────────────────────────────────
BUTTON_WIDTH = 260
BUTTON_HEIGHT = 60
BUTTON_BORDER_RADIUS = 12
BUTTON_SPACING = 20
