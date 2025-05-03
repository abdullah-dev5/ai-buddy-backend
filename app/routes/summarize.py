from fastapi import APIRouter
from pydantic import BaseModel
from app.services.summarize import handle_summarization

router = APIRouter()

class TextPayload(BaseModel):
    text: str

@router.post("/")
async def summarize_text(payload: TextPayload):
    result = await handle_summarization(payload.text)
    return result
