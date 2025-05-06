import httpx
import asyncio
import os
from app.config import HUGGINGFACE_API_TOKEN, TRANSCRIPTION_MODEL, MAX_RETRIES

async def check_model_status():
    """Verify model access and availability with proper headers"""
    API_URL = f"https://api-inference.huggingface.co/models/{TRANSCRIPTION_MODEL}"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Accept": "application/json"
    }
    
    print("\n🔍 Verifying Model Access:")
    print(f"• Model: {TRANSCRIPTION_MODEL}")
    print(f"• Token: {HUGGINGFACE_API_TOKEN[:6]}...")

    try:
        async with httpx.AsyncClient() as client:
            # Check model existence
            model_check = await client.get(
                f"https://huggingface.co/api/models/{TRANSCRIPTION_MODEL}",
                timeout=10
            )
            if model_check.status_code == 404:
                print(f"❌ Model not found: {TRANSCRIPTION_MODEL}")
                return False

            # Check API access
            api_check = await client.get(API_URL, headers=headers, timeout=10)
            if api_check.status_code == 200:
                print("✅ Full access verified!")
                return True
            print(f"❌ API access failed ({api_check.status_code})")
            return False
            
    except Exception as e:
        print(f"🚨 Connection failed: {str(e)}")
        return False

async def transcribe_chunk(chunk_path: str):
    """Transcribe with proper headers and error handling"""
    API_URL = f"https://api-inference.huggingface.co/models/{TRANSCRIPTION_MODEL}"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "audio/wav",  # CRITICAL FIX
        "Accept": "application/json"
    }

    for attempt in range(MAX_RETRIES):
        try:
            with open(chunk_path, "rb") as f:
                data = f.read()
                print(f"  Attempt {attempt+1} - Sending {len(data)/1024:.1f}KB")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    API_URL,
                    headers=headers,
                    content=data,
                    timeout=30
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 503:
                    wait = min(2 ** attempt, 30)
                    print(f"  ⏳ Model loading, waiting {wait}s...")
                    await asyncio.sleep(wait)
                    continue
                else:
                    print(f"  ❌ API error {response.status_code}: {response.text[:200]}")
                    return {"error": f"API error {response.status_code}"}

        except Exception as e:
            print(f"  ❌ Attempt {attempt+1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(min(2 ** attempt, 30))
    
    return {"error": "Max retries exceeded"}