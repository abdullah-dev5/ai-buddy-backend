import httpx
from app.config import HUGGINGFACE_API_TOKEN, SUMMARIZATION_MODEL

async def summarize_text(text: str):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": text}
    response = httpx.post(
        f"https://api-inference.huggingface.co/models/{SUMMARIZATION_MODEL}",
        headers=headers,
        json=payload
    )
    return response.json()
