import pygame

# ── Window ──────────────────────────────────────────────────────────────
WINDOW_TITLE = "Chess"
FPS = 60

# ── Colors (from docs/ui-mockups.md) ───────────────────────────────────
COLOR_BACKGROUND      = pygame.image.load("assets/BackgroundAlt.png")  # #f5dbb5
COLOR_PANEL           = (60, 58, 55)      # #3C3A37
COLOR_TEXT            = (0, 0, 0)         # #000000
COLOR_TEXT_DIM        = (180, 180, 180)
COLOR_BUTTON          = pygame.image.load("assets/Button.png")
COLOR_BUTTON_HOVER    = pygame.image.load("assets/ButtonHovered.png")
COLOR_BUTTON_DISABLED = pygame.image.load("assets/ButtonDisabled.png")
COLOR_BUTTON_TEXT     = (0, 0, 0)

# Board assets
LIGHT_SQUARE    = pygame.image.load("assets/LightTile.png")  # #F0D9B5
DARK_SQUARE     = pygame.image.load("assets/DarkTile.png")   # #B58863
BOARD_BORDER    = pygame.image.load("assets/BoardBorder.png")
BOARD_BORDER_P  = 64 

# ── Typography ─────────────────────────────────────────────────────────
FONT_NAME = "assets/Font/C_Gothic_Bold_Regular.ttf"  # Copperplate Gothic Bold Regular Font

FONT_SIZE_TITLE   = 172
FONT_SIZE_HEADING = 96
FONT_SIZE_BUTTON  = 64
FONT_SIZE_BODY    = 64
FONT_SIZE_SMALL   = 32

# ── Button Defaults ────────────────────────────────────────────────────
BUTTON_WIDTH        = 260
BUTTON_HEIGHT       = 60
BUTTON_SPACING      = 20
COLOR_BUTTON_BORDER   = (140, 135, 125)
