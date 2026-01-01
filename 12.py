from huggingface_hub import InferenceClient
import config 

def classifyText(text):
    client = InferenceClient(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", api_key=config.HF_API_KEY)
    result = client.text_classification(text=text)
    return result

if __name__ == "__main__":
    sampleText = "LIFE IS GOOD"
    result = classifyText(sampleText)
    print(result)