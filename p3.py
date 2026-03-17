import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-inpainting"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}


def restore_image(image_path, mask_path):
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            files={
                "image": img,
                "mask_image": mask
            },
            data={
                "prompt": "restore image, remove scratches, remove tears, clean, natural texture"
            }
        )

    if response.status_code != 200:
        print("Error:", response.text)
        return None

    return Image.open(BytesIO(response.content))


def main():
    print("=== Image Restoration Tool ===\n")

    image_path = input("Enter damaged image path: ").strip()
    mask_path = input("Enter mask image path: ").strip()

    print("\nRestoring image...\n")

    result = restore_image(image_path, mask_path)

    if result:
        result.save("restored.png")
        print("Saved as restored.png")
        result.show()
    else:
        print("Restoration failed")


if __name__ == "__main__":
    main()