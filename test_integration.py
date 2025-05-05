import requests
from pprint import pprint

def test_transcription(token, audio_path="sample.wav"):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large"
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(audio_path, "rb") as f:
        data = f.read(300*1024)  # First 300KB
        
    response = requests.post(API_URL, headers=headers, data=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        pprint(response.json())
    elif response.status_code == 401:
        print("Solutions:")
        print("1. Generate new token at https://huggingface.co/settings/tokens")
        print("2. Accept terms at https://huggingface.co/openai/whisper-tiny")
    else:
        print(response.text)

# Usage:
test_transcription("your_NEW_token")