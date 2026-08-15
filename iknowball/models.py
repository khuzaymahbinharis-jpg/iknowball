# id is the OpenRouter model slug sent in the request.
MODELS = [
    {
        "id": "qwen/qwen3-vl-32b-instruct",
        "label": "Qwen3 VL 32B Instruct",
    },
    {
        "id": "nvidia/nemotron-nano-12b-v2-vl:free",
        "label": "Nemotron Nano 12B VL (free)",
    },
    {
        "id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "label": "Nemotron 3 Nano Omni (free)",
    },
    {
        "id": "google/gemma-4-31b-it:free",
        "label": "Gemma 4 31B (free)",
    },
    {
        "id": "meta-llama/llama-4-scout",
        "label": "Llama 4 Scout",
    },
    {
        "id": "qwen/qwen2.5-vl-72b-instruct",
        "label": "Qwen2.5 VL 72B Instruct",
    },
]

DEFAULT_MODEL_ID = "qwen/qwen3-vl-32b-instruct"
MODEL_IDS = [m["id"] for m in MODELS]
FREE_MODEL_IDS = [m["id"] for m in MODELS if m["id"].endswith(":free")]
