import requests
from PIL import Image
from io import BytesIO
from colorama import init, Fore, Style
from config import HF_API_KEY  

init(autoreset=True)

MODEL = "Salesforce/blip-image-captioning-base"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_caption(image_path):
    try:
        with open(image_path, "rb") as img:
            r = requests.post(API_URL, headers=HEADERS, files={"file": img}, timeout=60)
        if r.status_code != 200:
            print(Fore.RED + f"API Error ({r.status_code}): {r.text[:200]}")
            return None
        return r.json().get("generated_text")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None

def expand_caption(basic_caption):
    return f"{basic_caption}. This image depicts a detailed scene with multiple elements and context, giving more information about the environment, actions, and objects involved in the picture, making it richer and more descriptive."

def main():
    print(Fore.CYAN + "=== AI Image Captioning Script ===")
    image_path = input("Enter image path: ").strip()

    caption = generate_caption(image_path)
    if not caption:
        print(Fore.RED + "Failed to generate caption.")
        return

    print(Fore.GREEN + f"Basic Caption: {caption}")

    expand = input("Do you want a longer 30-word description? (yes/no): ").strip().lower()
    if expand == "yes":
        long_caption = expand_caption(caption)
        print(Fore.YELLOW + f"Expanded Caption:\n{long_caption}")

if __name__ == "__main__":
    main()