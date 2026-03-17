import requests, time, random
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from config import HF_API_KEY


MODEL = "stabilityai/stable-diffusion-3-medium-diffusers"
URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Accept": "image/png",
    "Content-Type": "application/json"
}


def generate(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "seed": random.randint(0, 10**9)
        }
    }

    for i in range(5):
        try:
            r = requests.post(URL, headers=HEADERS, json=payload, timeout=120)
        except requests.RequestException as e:
            print("Request error:", e)
            return None

        content_type = r.headers.get("Content-Type", "")

        if r.status_code == 200 and "image" in content_type:
            return Image.open(BytesIO(r.content))

        try:
            print("API response:", r.json())
        except:
            print("Raw response:", r.text)

        if r.status_code == 503:
            print("Model loading... retrying")
            time.sleep(2 + i)
            continue

        break

    return None

def daylight_version(img):
    bright = ImageEnhance.Brightness(img).enhance(1.4)
    contrast = ImageEnhance.Contrast(bright).enhance(0.9)
    soft = contrast.filter(ImageFilter.GaussianBlur(radius=1))
    return soft


def night_version(img):
    contrast = ImageEnhance.Contrast(img).enhance(1.6)
    dark = ImageEnhance.Brightness(contrast).enhance(0.7)
    blur = dark.filter(ImageFilter.GaussianBlur(radius=2))
    return blur


def main():
    print("=== AI Image Tone Experiment ===\n")

    prompt = input("Enter your prompt: ").strip()

    print("\nGenerating base image...\n")
    base_img = generate(prompt)

    if base_img is None:
        print("Failed to generate image")
        return

    base_img.save("original.png")
    print("Saved original.png")

    day = daylight_version(base_img)
    night = night_version(base_img)

    day.save("daylight.png")
    night.save("night.png")

    print("Saved daylight.png (bright & soft)")
    print("Saved night.png (dark & cinematic)")

    base_img.show()
    day.show()
    night.show()


if __name__ == "__main__":
    main()