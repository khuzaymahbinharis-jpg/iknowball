from PIL import Image, ImageDraw


def outline_circle(
    image: Image.Image,
    cx: int,
    cy: int,
    r: int,
    *,
    color: tuple[int, int, int] = (0, 255, 80),
    width: int | None = None,
) -> Image.Image:
    drawn = image.copy().convert("RGB")
    if width is None:
        width = max(3, min(drawn.size) // 200)
    draw = ImageDraw.Draw(drawn)
    box = [cx - r, cy - r, cx + r, cy + r]
    draw.ellipse(box, outline=color, width=width)
    return drawn
