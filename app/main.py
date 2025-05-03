from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import transcribe, summarize, export

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder for exports
app.mount("/files", StaticFiles(directory="generated"), name="files")

# Include API routes
app.include_router(transcribe.router, prefix="/transcribe")
app.include_router(summarize.router, prefix="/summarize")
app.include_router(export.router, prefix="/export")
