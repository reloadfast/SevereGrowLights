"""
gen_textures.py — Generate 14 PNGs for SevereGrowLights mod
7 building sprites (64×64) + 7 architect UI icons (64×64)

Requires: Pillow  (pip install Pillow)
Run from repo root:  python Tools/gen_textures.py
"""

from PIL import Image, ImageDraw
import os
import math

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE_DIR = os.path.join(REPO_ROOT, "SevereGrowLights", "Textures", "Things", "Building", "Production")
ICON_DIR   = os.path.join(REPO_ROOT, "SevereGrowLights", "Textures", "UI", "Icons")
SIZE = 64

# ---------------------------------------------------------------------------
# Lamp definitions
# ---------------------------------------------------------------------------
#  name            shape          hw_colour    centre_colour
LAMPS = [
    {
        "name":     "SGL_IncandLamp",
        "shape":    "circle",
        "shape_r":  26,
        "housing":  (60, 60, 60),
        "centre":   (255, 210, 100),
        "label":    "Incandescent",
    },
    {
        "name":     "SGL_HalogenLamp",
        "shape":    "circle",
        "shape_r":  26,
        "housing":  (160, 160, 160),
        "centre":   (255, 240, 180),
        "label":    "Halogen",
    },
    {
        "name":     "SGL_SodiumLamp",
        "shape":    "oval",
        "oval_w":   52,
        "oval_h":   38,
        "housing":  (25, 20, 15),
        "centre":   (255, 140, 30),
        "label":    "Sodium",
    },
    {
        "name":     "SGL_LEDLampMkI",
        "shape":    "square",
        "sq_size":  48,
        "housing":  (30, 40, 60),
        "centre":   (180, 215, 255),
        "label":    "LED Mk I",
    },
    {
        "name":     "SGL_LEDLampMkI_Red",
        "shape":    "square",
        "sq_size":  48,
        "housing":  (40, 20, 30),
        "centre":   (200, 40, 80),
        "label":    "LED Red",
    },
    {
        "name":     "SGL_LEDLampMkI_Blue",
        "shape":    "square",
        "sq_size":  48,
        "housing":  (20, 25, 50),
        "centre":   (80, 150, 255),
        "label":    "LED Blue",
    },
    {
        "name":     "SGL_AdvancedLEDArray",
        "shape":    "adv",
        "adv_w":    56,
        "adv_h":    56,
        "housing":  (10, 12, 18),
        "centre":   (210, 238, 255),
        "label":    "Advanced LED",
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def lerp_colour(c1, c2, t):
    """Linear interpolate between two RGB tuples, return RGBA."""
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return (r, g, b, 255)


def add_glow(img, cx, cy, colour, radius, steps=12):
    """Paint a radial glow using concentric filled ellipses, outermost first."""
    draw = ImageDraw.Draw(img)
    for i in range(steps, 0, -1):
        t = i / steps          # 1.0 at edge → 0.0 at centre
        r = int(radius * t)
        alpha = int(200 * (1 - t) ** 1.5 + 30)
        # Fade to transparent at edge
        blend = lerp_colour(colour, (0, 0, 0), t * 0.6)
        glow_col = (blend[0], blend[1], blend[2], alpha)
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=glow_col,
        )


def draw_mount(draw, cx, colour):
    """Small mount bracket at top-centre (3 px wide, 6 px tall)."""
    bw, bh = 8, 6
    x0 = cx - bw // 2
    draw.rectangle([x0, 2, x0 + bw - 1, 2 + bh - 1], fill=colour + (255,))


def draw_bracket_ring(draw, cx, cy, r, colour, width=2):
    """Thin ring for housing outline."""
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        outline=colour + (255,),
        width=width,
    )

# ---------------------------------------------------------------------------
# Sprite generators per shape
# ---------------------------------------------------------------------------

def make_sprite_circle(lamp, padding=0):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    r = lamp["shape_r"] - padding
    hw = lamp["housing"]
    centre = lamp["centre"]

    # Glow behind housing
    add_glow(img, cx, cy, centre, r + 10)

    # Housing disc (4 fill steps from edge to centre)
    steps = 4
    for i in range(steps, -1, -1):
        t = i / steps
        col = lerp_colour(hw, centre, 1 - t)
        rr = int(r * t + 2)
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)

    # Bright centre spot
    spot = 6 - padding // 2
    draw.ellipse([cx - spot, cy - spot, cx + spot, cy + spot], fill=centre + (255,))

    # Housing ring
    draw_bracket_ring(draw, cx, cy, r, hw)

    # Mount
    draw_mount(draw, cx, hw)
    return img


def make_sprite_oval(lamp, padding=0):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    hw_w = (lamp["oval_w"] - padding * 2) // 2
    hw_h = (lamp["oval_h"] - padding * 2) // 2
    hw = lamp["housing"]
    centre = lamp["centre"]

    # Glow
    add_glow(img, cx, cy, centre, max(hw_w, hw_h) + 10)

    # Housing — oval fill steps
    steps = 4
    for i in range(steps, -1, -1):
        t = i / steps
        col = lerp_colour(hw, centre, 1 - t)
        rw = max(1, int(hw_w * t))
        rh = max(1, int(hw_h * t))
        draw.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=col)

    # Bright centre
    draw.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=centre + (255,))

    # Housing ring
    draw.ellipse([cx - hw_w, cy - hw_h, cx + hw_w, cy + hw_h], outline=hw + (255,), width=2)

    draw_mount(draw, cx, hw)
    return img


def make_sprite_square(lamp, padding=0):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    half = (lamp["sq_size"] - padding * 2) // 2
    hw = lamp["housing"]
    centre = lamp["centre"]

    # Glow (ellipse behind square panel)
    add_glow(img, cx, cy, centre, half + 8)

    # LED panel housing fill
    draw.rectangle([cx - half, cy - half, cx + half, cy + half], fill=hw + (255,))

    # Inner LED cells (3×3 grid of small lit squares)
    cell = (half * 2 - 4) // 3
    for row in range(3):
        for col in range(3):
            x0 = cx - half + 2 + col * (cell + 1)
            y0 = cy - half + 2 + row * (cell + 1)
            # Vary brightness slightly per cell
            brightness = 0.7 + 0.3 * ((row + col) % 2)
            cr = int(centre[0] * brightness)
            cg = int(centre[1] * brightness)
            cb = int(centre[2] * brightness)
            draw.rectangle([x0, y0, x0 + cell, y0 + cell], fill=(cr, cg, cb, 230))

    # Centre brighter pixel cluster
    draw.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=centre + (255,))

    # Outline
    draw.rectangle([cx - half, cy - half, cx + half, cy + half], outline=hw + (200,), width=1)

    draw_mount(draw, cx, hw)
    return img


def make_sprite_adv(lamp, padding=0):
    """Advanced LED Array: outer rect + inner 3×3 sub-panel grid with frame."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    hw_w = (lamp["adv_w"] - padding * 2) // 2
    hw_h = (lamp["adv_h"] - padding * 2) // 2
    hw = lamp["housing"]
    centre = lamp["centre"]

    # Wide glow
    add_glow(img, cx, cy, centre, hw_w + 12, steps=16)

    # Outer housing
    draw.rectangle([cx - hw_w, cy - hw_h, cx + hw_w, cy + hw_h], fill=hw + (255,))

    # 3×3 sub-panel grid with 2 px gutters
    panel_area_w = hw_w * 2 - 8
    panel_area_h = hw_h * 2 - 8
    cell_w = (panel_area_w - 4) // 3   # 2 gutters
    cell_h = (panel_area_h - 4) // 3
    gutter = 2
    x_start = cx - hw_w + 4
    y_start = cy - hw_h + 4

    for row in range(3):
        for col in range(3):
            x0 = x_start + col * (cell_w + gutter)
            y0 = y_start + row * (cell_h + gutter)
            # Alternate brightness
            brightness = 0.75 + 0.25 * ((row * 3 + col) % 3) / 2
            cr = int(centre[0] * brightness)
            cg = int(centre[1] * brightness)
            cb = int(centre[2] * brightness)
            draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=(cr, cg, cb, 240))
            # Inner highlight
            draw.rectangle([x0 + 1, y0 + 1, x0 + cell_w - 1, y0 + cell_h - 1],
                           outline=(255, 255, 255, 60), width=1)

    # Bright centre
    draw.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=centre + (255,))

    # Outer frame
    draw.rectangle([cx - hw_w, cy - hw_h, cx + hw_w, cy + hw_h],
                   outline=(80, 100, 120, 200), width=2)

    draw_mount(draw, cx, hw)
    return img

# ---------------------------------------------------------------------------
# Icon variant — same logic but tighter (4 px padding crop)
# ---------------------------------------------------------------------------
ICON_PADDING = 4


def make_image(lamp, icon=False):
    padding = ICON_PADDING if icon else 0
    shape = lamp["shape"]
    if shape == "circle":
        return make_sprite_circle(lamp, padding)
    elif shape == "oval":
        return make_sprite_oval(lamp, padding)
    elif shape == "square":
        return make_sprite_square(lamp, padding)
    elif shape == "adv":
        return make_sprite_adv(lamp, padding)
    raise ValueError(f"Unknown shape: {shape}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(SPRITE_DIR, exist_ok=True)
    os.makedirs(ICON_DIR, exist_ok=True)

    for lamp in LAMPS:
        # Building sprite
        sprite_path = os.path.join(SPRITE_DIR, lamp["name"] + ".png")
        sprite = make_image(lamp, icon=False)
        sprite.save(sprite_path)
        print(f"  [sprite] {os.path.relpath(sprite_path, REPO_ROOT)}")

        # UI icon
        icon_path = os.path.join(ICON_DIR, lamp["name"] + ".png")
        icon = make_image(lamp, icon=True)
        icon.save(icon_path)
        print(f"  [icon]   {os.path.relpath(icon_path, REPO_ROOT)}")

    print(f"\nDone — {len(LAMPS) * 2} PNGs written.")


if __name__ == "__main__":
    main()
