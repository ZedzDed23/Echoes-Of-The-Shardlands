# src/palette.py
# Zork-style with modern aesthetics:
# Deep void backgrounds, phosphor-green/amber primary text, colour-coded importance.
# Format: (R, G, B)

# ── Terminal / Zork Core ──────────────────────────────────────────────────────
TERMINAL_GREEN  = (0,   230,  80)   # Classic phosphor green – main body text
TERMINAL_AMBER  = (255, 176,   0)   # CRT amber – warnings, items, rewards
TERMINAL_DIM    = (0,   140,  50)   # Dimmer green – secondary/flavour text
DEEP_VOID       = (5,     5,  15)   # Near-black – primary background
BONE_WHITE      = (225, 215, 195)   # Off-white parchment – important NPC text
EMBER_RED       = (220,  50,  30)   # Danger, enemies, death

# ── Fantasy Accent (kept for visual identity) ────────────────────────────────
SOLAR_GOLD      = (255, 215,   0)   # Player highlight, legendary items
CRYSTAL_BLUE    = (0,   191, 255)   # Magical effects, teleport
SUNBEAM_YELLOW  = (255, 250, 205)   # Player pulse animation
FAE_PINK        = (255, 105, 180)   # NPCs
SHADOW_PURPLE   = (102,  51, 153)   # Legendary rarity, special events
CRYSTAL_TEAL    = (0,   200, 180)   # Special reward confirmations
FADED_GOLD      = (180, 150,  60)   # UI borders, muted accent

# ── Structural / Room colours ─────────────────────────────────────────────────
ANCIENT_STONE_GREY = (90,  90, 100) # Room floor (darker, more atmospheric)
RUSTIC_BROWN       = (110, 55,  20) # Room walls
DIM_STONE          = (55,  55,  65) # Mini-boss / dark room floor
MOSSY_GREEN        = (45,  80,  45) # Rest area / library floor

# ── Legacy aliases (keep for backward-compat in game.py) ─────────────────────
FOREST_GREEN    = (34,  139,  34)
LIGHT_TEXT      = (225, 215, 195)   # Same as BONE_WHITE
DARK_BACKGROUND = (5,     5,  15)   # Same as DEEP_VOID
error_red       = (200,   0,   0)

PALETTE = {
    "terminal_green":  (0,   230,  80),
    "terminal_amber":  (255, 176,   0),
    "terminal_dim":    (0,   140,  50),
    "deep_void":       (5,     5,  15),
    "bone_white":      (225, 215, 195),
    "ember_red":       (220,  50,  30),
    "solar_gold":      (255, 215,   0),
    "crystal_blue":    (0,   191, 255),
    "sunbeam_yellow":  (255, 250, 205),
    "fae_pink":        (255, 105, 180),
    "shadow_purple":   (102,  51, 153),
    "crystal_teal":    (0,   200, 180),
    "faded_gold":      (180, 150,  60),
    "ancient_stone":   (90,   90, 100),
    "rustic_brown":    (110,  55,  20),
    "dim_stone":       (55,   55,  65),
    "mossy_green":     (45,   80,  45),
    "light_text":      (225, 215, 195),
    "dark_bg":         (5,    5,   15),
    "error_red":       (200,   0,   0),
}
