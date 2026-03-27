import requests
import time
import os
from config import HF_API_KEY

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def caption_image(image_path):
    API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"

    if not os.path.exists(image_path):
        print("❌ Image not found. Check path.")
        return None

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    for attempt in range(5): 
        try:
            print(f"🔄 Attempt {attempt+1}...")
            response = requests.post(
                API_URL,
                headers=headers,
                data=image_bytes,
                timeout=60
            )

            if response.status_code == 503:
                print("⏳ Model is loading... retrying")
                time.sleep(5)
                continue

            if response.status_code != 200:
                print("❌ API Error:", response.text)
                return None
            result = response.json()
            return result[0]["generated_text"]
        except requests.exceptions.RequestException as e:
            print("⚠️ Network error:", e)
            time.sleep(3)

    print("❌ Failed after retries.")
    return None

def generate_story(prompt):
    API_URL = "https://api-inference.huggingface.co/models/gpt2"

    payload = {
        "inputs": f"Write a short creative story based on: {prompt}",
        "parameters": {
            "max_length": 120,
            "temperature": 0.9
        }
    }
    
    for attempt in range(5):
        try:
            print(f"🔄 Story attempt {attempt+1}...")
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 503:
                print("⏳ Model loading... retrying")
                time.sleep(5)
                continue

            if response.status_code != 200:
                print("❌ API Error:", response.text)
                return None
            result = response.json()
            return result[0]["generated_text"]
        except requests.exceptions.RequestException as e:
            print("⚠️ Network error:", e)
            time.sleep(3)

    print("❌ Failed to generate story.")
    return None

def main():
    print("🔥 AI Caption + Story Generator\n")

    image_path = input("📂 Enter image path: ").strip()
    print("\n🔍 Generating caption...")
    caption = caption_image(image_path)

    if not caption:
        print("❌ Could not generate caption.")
        return
    print("\n📝 Caption:", caption)

    print("\n✨ Generating story...")
    story = generate_story(caption)
    if not story:
        print("❌ Could not generate story.")
        return

    print("\n📖 AI Story:\n")
    print(story)
    
if __name__ == "__main__":
    main()