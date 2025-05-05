from dotenv import load_dotenv
import os

load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
TRANSCRIPTION_MODEL = "openai/whisper-large-v3"
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
MAX_RETRIES = 3  # Number of retry attempts
CHUNK_DURATION = 30  # Seconds per chunk
CHUNK_DELAY = 5  # seconds between API calls
