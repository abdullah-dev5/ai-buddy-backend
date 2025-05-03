from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    transcription: str

class SummarizationRequest(BaseModel):
    text: str

class SummarizationResponse(BaseModel):
    summary: str
