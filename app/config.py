from dotenv import load_dotenv
import os

load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
TRANSCRIPTION_MODEL = "openai/whisper-base"
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
