# app/services/transcribe.py
from fastapi import UploadFile
from app.utils.whisper_api import transcribe_via_whisper

async def handle_transcription(file: UploadFile):
    result = await transcribe_via_whisper(file)
    if isinstance(result, dict) and 'text' in result:
        return {"status": "success", "transcript": result['text']}
    elif isinstance(result, dict) and 'error' in result:
        return {"status": "error", "message": result['error']}
    else:
        return {"status": "error", "message": "Unknown response format"}