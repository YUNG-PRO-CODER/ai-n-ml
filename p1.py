import requests, time, random
from PIL import Image
from io import BytesIO
from config import HF_API_KEY


class HFImageClient:
    def __init__(self):
        self.model = "stabilityai/stable-diffusion-3-medium-diffusers"
        self.url = f"https://router.huggingface.co/hf-inference/models/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Accept": "image/png",
            "Content-Type": "application/json"
        }

    def create(self, data):
        for retry in range(3):
            try:
                res = requests.post(self.url, headers=self.headers, json=data, timeout=120)
            except requests.RequestException as e:
                return None, str(e)

            if res.status_code == 200 and "image" in res.headers.get("Content-Type", ""):
                return Image.open(BytesIO(res.content)), None

            if res.status_code in (502, 503, 504):
                time.sleep(1 + retry)
                continue

            return None, self._error(res)

        return None, "Max retries exceeded"

    def _error(self, res):
        try:
            j = res.json()
            return j.get("error", str(j))
        except:
            return res.text or res.reason


class PromptEngine:
    styles = {
        "anime": "anime style, vibrant, sharp lines",
        "realistic": "photorealistic, ultra detailed",
        "cyberpunk": "cyberpunk, neon lighting, futuristic",
        "fantasy": "fantasy art, epic lighting",
        "dark": "dark cinematic shadows, moody"
    }

    default_neg = "blurry, low quality, bad anatomy, extra fingers, watermark"

    @classmethod
    def build(cls, text, style=None):
        if style in cls.styles:
            return f"{text}, {cls.styles[style]}"
        return text


def payload_factory(prompt, neg, steps, scale, w, h, seed):
    return {
        "inputs": prompt,
        "parameters": dict(
            negative_prompt=neg,
            num_inference_steps=steps,
            guidance_scale=scale,
            width=w,
            height=h,
            seed=seed
        )
    }


def get_int(value, default):
    return int(value) if value.isdigit() else default


def get_float(value, default):
    try:
        return float(value)
    except:
        return default


def parse_size(text):
    if "x" in text:
        try:
            w, h = map(int, text.split("x"))
            return w, h
        except:
            pass
    return 512, 512


def run():
    client = HFImageClient()

    print("=== HF Generator v2 ===\n")

    while True:
        text = input("Prompt: ").strip()
        if text.lower() == "exit":
            break

        style = input("Style: ").strip().lower()
        neg = input("Negative (optional): ").strip()

        steps = get_int(input("Steps: ").strip(), 30)
        scale = get_float(input("Guidance: ").strip(), 7.5)
        width, height = parse_size(input("Size (e.g. 512x512): ").strip())

        if not neg:
            neg = PromptEngine.default_neg

        final_prompt = PromptEngine.build(text, style)
        seed = random.randint(0, 10**9)

        data = payload_factory(final_prompt, neg, steps, scale, width, height, seed)

        print("\nGenerating...\n")

        image, err = client.create(data)

        if err:
            print("Error:", err, "\n")
            continue

        print("Seed:", seed)
        image.show()

        if input("Save? ").lower() == "yes":
            name = input("Filename: ").strip() or "img"
            name = "".join(c for c in name if c.isalnum() or c in "_-")
            image.save(f"{name}.png")
            print("Saved\n")

        print("-" * 50)


if __name__ == "__main__":
    run()