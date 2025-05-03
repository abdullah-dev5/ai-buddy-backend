from app.utils.huggingface_api import summarize_text

async def handle_summarization(text: str):
    return await summarize_text(text)
