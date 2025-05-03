from fastapi import APIRouter, UploadFile, File
from app.services.transcribe import handle_transcription

router = APIRouter()

@router.post("/")
async def transcribe_audio(file: UploadFile = File(...)):
    result = await handle_transcription(file)
    return result
