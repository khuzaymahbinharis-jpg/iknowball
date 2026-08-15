# iknowball

Upload a photo of a ball. A vision model returns a circle (`cx`, `cy`, `r`); Pillow draws it on the original image.

## Run

You need Python 3.11+ and an [OpenRouter](https://openrouter.ai) API key.

```powershell
git clone https://github.com/khuzaymahbinharis-jpg/iknowball.git
cd iknowball

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux, use `python3 -m venv .venv` then `source .venv/bin/activate`.

Copy `.env.example` to `.env` and paste your key:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

Start the app:

```powershell
streamlit run iknowball/app.py
```

Open the URL it prints (usually http://localhost:8501). Pick a model, upload an image, click **Outline ball**.

The dropdown defaults to **Nemotron Nano 12B VL (free)**. Free models can be slow or rate-limited; if one fails, try **Nemotron 3 Nano Omni (free)** or **Qwen3 VL 32B Instruct**.

Do not commit `.env`.
