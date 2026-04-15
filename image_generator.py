import os
import time
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY not set. Please check your .env file.")

client = InferenceClient(api_key=HF_API_KEY)

STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)


def stable_filename(prompt: str):
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    return STATIC_DIR / f"{digest}.png"


def generate_image(prompt: str, retries: int = 3, sleep_seconds: int = 5):
    output_path = stable_filename(prompt)

    if output_path.exists():
        return str(output_path)

    last_error = None

    for attempt in range(retries):
        try:
            image = client.text_to_image(
                prompt,
                model=HF_MODEL,
            )

            image.save(output_path)
            return str(output_path)

        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(sleep_seconds)

    print("Image generation failed after retries:", last_error)
    return None