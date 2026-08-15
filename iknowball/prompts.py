def circle_prompt() -> str:
    return """Return JSON only. No markdown. No commentary.
Put "where" first, then the numbers.

{"where": "<one sentence: which part of the image, what the ball touches, roughly how wide vs the frame>", "cx": 0, "cy": 0, "r": 0}

COORDINATES (0-1000 scale, origin top-left)
- cx: 0 is the left edge, 1000 is the right edge
- cy: 0 is the top edge, 1000 is the bottom edge
- r: radius if the shorter side of the image is 1000 units
Do not use this photo's pixel width/height. Do not use 0-1.

Example (not this image):
{"where": "orange basketball on the left of the shoes, sitting on the court, about a quarter of the frame wide", "cx": 280, "cy": 620, "r": 190}

TASK
Find the one primary sports ball (basketball, soccer, football, tennis, baseball, volleyball, rugby, or similar).
Return a circle on the ball: center at the ball's center, radius to the outer rim.

- The real ball, never its reflection, shadow, watermark, shoes, person, or animal.
- If something covers part of the ball, still give the full ball's center and radius, not the occluder.
- r must be the ball radius, not a box around nearby objects.

JSON only:
{"where": "...", "cx": 0, "cy": 0, "r": 0}"""
