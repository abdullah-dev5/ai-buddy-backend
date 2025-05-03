import tempfile
import aiofiles
from fastapi import UploadFile
from app.config import HUGGINGFACE_API_TOKEN, TRANSCRIPTION_MODEL
import httpx

import httpx
from app.config import HUGGINGFACE_API_TOKEN, TRANSCRIPTION_MODEL

async def transcribe_via_whisper(file):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api-inference.huggingface.co/models/{TRANSCRIPTION_MODEL}",
                headers=headers,
                content=await file.read(),
            )
            
            # Log the raw response content
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content.decode()}")

            # Check for a successful response (HTTP 200)
            if response.status_code == 200:
                return response.json()
            else:
                # Handle cases where the API returns an error
                return {"error": f"Failed to transcribe, status code: {response.status_code}, message: {response.text}"}
    
    except httpx.RequestError as e:
        return {"error": f"An error occurred while sending the request: {str(e)}"}
