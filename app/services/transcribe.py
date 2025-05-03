from fastapi import UploadFile
from app.utils.whisper_api import transcribe_via_whisper

async def handle_transcription(file: UploadFile):
    return await transcribe_via_whisper(file)
