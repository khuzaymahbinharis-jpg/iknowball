import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from iknowball.config import load_env
from iknowball.locate import locate_ball
from iknowball.models import FREE_MODEL_IDS

load_env()

IMAGES = Path(r"C:\Users\salar\OneDrive\Desktop\Uni Work\Zeta Internship\test images")
OUT = ROOT / "uploads"
OUT.mkdir(exist_ok=True)

# 1.webp is the same scene as 1.jpg
files = [IMAGES / "1.jpg", IMAGES / "2.jpg", IMAGES / "3.jpg"]
models = sys.argv[1:] or FREE_MODEL_IDS


def slug(model: str) -> str:
    return model.replace("/", "_").replace(":", "_")


for image_path in files:
    image = Image.open(image_path).convert("RGB")
    for model in models:
        print(f"START {image_path.name} | {model}", flush=True)
        try:
            result = locate_ball(image, model)
        except Exception as exc:
            print(f"FAIL  {image_path.name} | {model} | {type(exc).__name__}: {exc}", flush=True)
            continue

        tag = result.unit or "none"
        if result.error:
            print(
                f"PARSE {image_path.name} | {model} | {tag} | {result.error}",
                flush=True,
            )
        else:
            dest = OUT / f"{image_path.stem}__{slug(model)}__{tag}.png"
            result.image.save(dest)
            print(
                f"OK    {image_path.name} | {model} | {tag} | "
                f"unit={result.unit} cx={result.cx} cy={result.cy} r={result.r} | {dest.name}",
                flush=True,
            )
        preview = result.raw_first.replace("\n", " ")[:180]
        print(f"TEXT  {preview}", flush=True)
        if result.raw_retry:
            preview_r = result.raw_retry.replace("\n", " ")[:180]
            print(f"RETRY {preview_r}", flush=True)
