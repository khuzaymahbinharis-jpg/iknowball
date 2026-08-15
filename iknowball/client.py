import base64
import io
import os

from openai import OpenAI
from PIL import Image

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

CIRCLE_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "ball_circle",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "where": {"type": "string"},
                "cx": {"type": "number"},
                "cy": {"type": "number"},
                "r": {"type": "number"},
            },
            "required": ["where", "cx", "cy", "r"],
            "additionalProperties": False,
        },
    },
}


def get_client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Put it in .env")
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=key,
        timeout=120.0,
        default_headers={
            "HTTP-Referer": "https://github.com/khuzaymahbinharis-jpg/iknowball",
            "X-Title": "iknowball",
        },
    )


def image_to_data_url(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.convert("RGB").save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def chat_with_image(image: Image.Image, model: str, prompt: str) -> str:
    client = get_client()
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": image_to_data_url(image)},
                },
                {"type": "text", "text": prompt},
            ],
        }
    ]
    base = {
        "model": model,
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0,
    }

    response = None
    last_error: Exception | None = None
    for fmt in (CIRCLE_JSON_SCHEMA, {"type": "json_object"}, None):
        kwargs = dict(base)
        if fmt is not None:
            kwargs["response_format"] = fmt
        try:
            response = client.chat.completions.create(**kwargs)
            break
        except Exception as exc:
            last_error = exc
            print(f"WARN response_format failed ({fmt}): {exc}", flush=True)
            continue
    if response is None:
        raise last_error or RuntimeError("OpenRouter call failed")

    if response.usage:
        print(
            f"USAGE prompt={response.usage.prompt_tokens} "
            f"completion={response.usage.completion_tokens}",
            flush=True,
        )
    if not response.choices:
        raise RuntimeError("Model returned no choices")
    message = response.choices[0].message
    text = None if message is None else message.content
    if not text or not str(text).strip():
        raise RuntimeError("Model returned empty text")
    return str(text)
