from dataclasses import dataclass

from PIL import Image

from iknowball.client import chat_with_image
from iknowball.draw import outline_circle
from iknowball.parse import (
    circle_to_pixels,
    circle_usable,
    infer_unit,
    parse_circle,
)
from iknowball.prompts import circle_prompt


@dataclass
class LocateResult:
    image: Image.Image
    points: list[tuple[int, int]]
    raw_first: str
    raw_retry: str | None
    used_retry: bool
    error: str | None = None
    where: str = ""
    unit: str = ""
    cx: int | None = None
    cy: int | None = None
    r: int | None = None


def locate_ball(image: Image.Image, model: str) -> LocateResult:
    rgb = image.convert("RGB")
    width, height = rgb.size
    raw = chat_with_image(rgb, model, circle_prompt())

    try:
        circle = parse_circle(raw)
    except ValueError as exc:
        return LocateResult(
            image=rgb,
            points=[],
            raw_first=raw,
            raw_retry=None,
            used_retry=False,
            error=str(exc),
        )

    unit = infer_unit(circle)
    cx, cy, r = circle_to_pixels(circle, width, height, unit)
    if not circle_usable(cx, cy, r, width, height):
        return LocateResult(
            image=rgb,
            points=[],
            raw_first=raw,
            raw_retry=None,
            used_retry=False,
            error=f"unusable circle unit={unit} cx={cx} cy={cy} r={r}",
            where=circle.where,
            unit=unit,
            cx=cx,
            cy=cy,
            r=r,
        )

    return LocateResult(
        image=outline_circle(rgb, cx, cy, r),
        points=[(cx, cy)],
        raw_first=raw,
        raw_retry=None,
        used_retry=False,
        where=circle.where,
        unit=unit,
        cx=cx,
        cy=cy,
        r=r,
    )
