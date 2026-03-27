from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os
import sys

print("🔄 Loading models... (first time may take time)")

try:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    text_generator = pipeline(
        "text-generation",
        model="gpt2",
        device=0 if torch.cuda.is_available() else -1
    )

    print("✅ Models loaded successfully!\n")

except Exception as e:
    print("❌ Error loading models:", e)
    sys.exit()

def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Image not found. Check path again.")
    
    try:
        image = Image.open(path).convert('RGB')
        return image
    except Exception:
        raise ValueError("Invalid image file.")


def generate_caption(image):
    try:
        inputs = processor(image, return_tensors="pt")
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        raise RuntimeError(f"Caption generation failed: {e}")


def generate_story(caption):
    try:
        prompt = f"Write a creative and detailed story about: {caption}"

        result = text_generator(
            prompt,
            max_new_tokens=150,
            num_return_sequences=1,
            temperature=0.9,
            top_k=50,
            top_p=0.95
        )

        story = result[0]['generated_text']

        story = story.replace(prompt, "").strip()

        return story

    except Exception as e:
        raise RuntimeError(f"Story generation failed: {e}")


def main():

    print("🧠 AI Image → Story Generator\n")

    while True:
        try:
            image_path = input("📂 Enter image path (or 'exit'): ").strip()

            if image_path.lower() == "exit":
                print("👋 Exiting...")
                break
            
            image = load_image(image_path)

            print("\n🖼️ Generating caption...")
            caption = generate_caption(image)
            print(f"🖼️ Caption: {caption}")

            print("\n📖 Generating story...")
            story = generate_story(caption)

            print("\n" + "="*50)
            print("📖 STORY OUTPUT:\n")
            print(story)
            print("="*50 + "\n")

        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()