import json
import re
from dataclasses import dataclass
from typing import Any, Literal

Unit = Literal["unit", "thousand", "pixels"]


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        data = json.loads(fenced.group(1))
        if isinstance(data, dict):
            return data

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        data = json.loads(text[start : end + 1])
        if isinstance(data, dict):
            return data

    raise ValueError("No JSON object in model output")


@dataclass
class Circle:
    where: str
    cx: float
    cy: float
    r: float


def parse_circle(text: str) -> Circle:
    data = extract_json_object(text)
    try:
        cx = float(data["cx"])
        cy = float(data["cy"])
        r = float(data["r"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("JSON needs numeric cx, cy, r") from exc
    where = data.get("where", "")
    if where is None:
        where = ""
    return Circle(where=str(where), cx=cx, cy=cy, r=r)


def infer_unit(circle: Circle) -> Unit:
    magnitude = max(abs(circle.cx), abs(circle.cy), abs(circle.r))
    if magnitude <= 1.5:
        return "unit"
    if magnitude <= 1000:
        return "thousand"
    return "pixels"


def circle_to_pixels(
    circle: Circle, width: int, height: int, unit: Unit
) -> tuple[int, int, int]:
    short = min(width, height)
    if unit == "unit":
        cx = circle.cx * width
        cy = circle.cy * height
        r = circle.r * short
    elif unit == "thousand":
        cx = circle.cx / 1000 * width
        cy = circle.cy / 1000 * height
        r = circle.r / 1000 * short
    else:
        cx, cy, r = circle.cx, circle.cy, circle.r
    return int(round(cx)), int(round(cy)), max(1, int(round(r)))


def circle_usable(cx: int, cy: int, r: int, width: int, height: int) -> bool:
    if r < 2 or r > max(width, height):
        return False
    return 0 <= cx < width and 0 <= cy < height
