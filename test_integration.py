import asyncio
from app.utils.huggingface_api import summarize_text
from app.utils.whisper_api import transcribe_via_whisper

async def test_all():
    # Test summarization
    text = "FastAPI is a modern, high-performance web framework for building APIs with Python."
    summary = await summarize_text(text)
    print("Summary:", summary)

    # Test transcription
    import aiofiles
    class DummyFile:
        def __init__(self, path):
            self.path = path

        async def read(self):
            async with aiofiles.open(self.path, "rb") as f:
                return await f.read()

    dummy_file = DummyFile("countdown.mp3")
    transcription = await transcribe_via_whisper(dummy_file)
    print("Transcription:", transcription)

asyncio.run(test_all())
