import pygame

# ── Window ──────────────────────────────────────────────────────────────
WINDOW_TITLE = "Chess"
FPS = 60

# ── Colors (from docs/ui-mockups.md) ───────────────────────────────────
COLOR_BACKGROUND      = (49, 46, 43)      # #312E2B
COLOR_PANEL           = (60, 58, 55)      # #3C3A37
COLOR_TEXT            = (255, 255, 255)   # #FFFFFF
COLOR_TEXT_DIM        = (180, 180, 180)
COLOR_BUTTON          = pygame.image.load("assets/Button.png")
COLOR_BUTTON_HOVER    = pygame.image.load("assets/ButtonHovered.png")
COLOR_BUTTON_DISABLED = pygame.image.load("assets/ButtonDisabled.png")
COLOR_BUTTON_TEXT     = (255, 255, 255)

# Board assets
LIGHT_SQUARE    = pygame.image.load("assets/LightTile.png")  # #F0D9B5
DARK_SQUARE     = pygame.image.load("assets/DarkTile.png")   # #B58863
BOARD_BORDER    = pygame.image.load("assets/BoardBorder.png")
BOARD_BORDER_P  = 64 

# ── Typography ─────────────────────────────────────────────────────────
FONT_NAME = None  # Pygame default; swap to a .ttf path for custom fonts

FONT_SIZE_TITLE   = 72
FONT_SIZE_HEADING = 48
FONT_SIZE_BUTTON  = 32
FONT_SIZE_BODY    = 24
FONT_SIZE_SMALL   = 18

# ── Button Defaults ────────────────────────────────────────────────────
BUTTON_WIDTH        = 260
BUTTON_HEIGHT       = 60
BUTTON_SPACING      = 20
COLOR_BUTTON_BORDER   = (140, 135, 125)
