from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from iknowball.config import load_env
from iknowball.locate import locate_ball
from iknowball.models import DEFAULT_MODEL_ID, MODELS

load_env()

st.set_page_config(page_title="iknowball", layout="centered")
st.title("iknowball")
st.caption("Circle prior (cx, cy, r) on a 0–1000 scale. Pillow draws the ring.")

model_labels = {m["label"]: m["id"] for m in MODELS}
choice = st.selectbox("Model", list(model_labels.keys()), index=1)
model_id = model_labels[choice]
st.caption(f"OpenRouter slug: `{model_id}`")
if model_id != DEFAULT_MODEL_ID:
    st.caption(f"Default in `.env` is `{DEFAULT_MODEL_ID}`.")

uploaded = st.file_uploader("Image", type=["png", "jpg", "jpeg", "webp"])
if uploaded is None:
    st.stop()

image = Image.open(uploaded).convert("RGB")
st.image(image, caption=f"{image.width} × {image.height} px", use_container_width=True)

if st.button("Outline ball", type="primary"):
    with st.spinner(f"Asking {model_id}…"):
        try:
            result = locate_ball(image, model_id)
        except Exception as exc:
            st.error(str(exc))
            st.stop()

    if result.error:
        st.error(result.error)
    else:
        st.image(
            result.image,
            caption=f"{result.unit}  cx={result.cx} cy={result.cy} r={result.r}",
            use_container_width=True,
        )
        if result.where:
            st.write(result.where)

    with st.expander("Model text"):
        st.code(result.raw_first, language="json")
