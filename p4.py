import os
import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY

MODEL = "Salesforce/blip-image-captioning-base"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")


def generate_caption(image_path):
    with open(image_path, "rb") as img_file:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            files={"file": img_file},
            timeout=60
        )

    if response.status_code != 200:
        print(f"Error with {image_path}: {response.status_code}")
        print("Response:", response.text[:200])
        return None

    try:
        return response.json().get("generated_text")
    except Exception as e:
        print(f"Failed to parse caption for {image_path}: {e}")
        return None


def main():
    print("=== Batch AI Image Captioning ===\n")
    folder = input("Enter the folder path containing images: ").strip()

    if not os.path.isdir(folder):
        print("Folder not found.")
        return

    images = [f for f in os.listdir(folder) if f.lower().endswith(VALID_EXTENSIONS)]
    if not images:
        print("No valid images found in the folder.")
        return

    summary_file = os.path.join(folder, "captions_summary.txt")
    with open(summary_file, "w", encoding="utf-8") as f_out:
        for img_name in images:
            img_path = os.path.join(folder, img_name)
            print(f"Processing {img_name}...")

            caption = generate_caption(img_path)
            if caption:
                f_out.write(f"{img_name} => {caption}\n")
                print(f"Caption: {caption}\n")
            else:
                f_out.write(f"{img_name} => FAILED\n")
                print("Captioning failed.\n")

    print(f"All done! Captions saved in: {summary_file}")


if __name__ == "__main__":
    main()