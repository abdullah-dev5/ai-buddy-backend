import wave
import math
import os
import tempfile
from typing import List

def validate_wav(file_path: str):
    """Validate WAV format meets API requirements"""
    try:
        with wave.open(file_path, 'rb') as wav:
            if wav.getsampwidth() != 2:
                raise ValueError("Must be 16-bit PCM (sample width=2)")
            if wav.getnchannels() not in [1, 2]:
                raise ValueError("Must be mono or stereo")
    except Exception as e:
        raise ValueError(f"Invalid WAV: {str(e)}")

def split_audio(file_path: str, chunk_sec: int) -> List[str]:
    """Split audio into chunks with validation"""
    validate_wav(file_path)
    
    chunk_dir = tempfile.mkdtemp(prefix="whisper_chunks_")
    chunks = []

    try:
        with wave.open(file_path, 'rb') as wav:
            params = wav.getparams()
            frames_per_chunk = chunk_sec * params.framerate
            
            for i in range(0, params.nframes, frames_per_chunk):
                chunk_path = os.path.join(chunk_dir, f"chunk_{len(chunks)}.wav")
                
                with wave.open(chunk_path, 'wb') as chunk:
                    chunk.setparams(params)
                    wav.setpos(i)
                    chunk.writeframes(wav.readframes(frames_per_chunk))
                
                chunks.append(chunk_path)
                print(f"  • Chunk {len(chunks)}: {os.path.getsize(chunk_path)/1024:.1f}KB")

        return chunks

    except Exception:
        clean_up_chunks(chunks)
        raise

def clean_up_chunks(chunks: List[str]):
    """Clean up temporary files"""
    if chunks:
        for chunk in chunks:
            try: os.unlink(chunk)
            except: pass
        try: os.rmdir(os.path.dirname(chunks[0]))
        except: pass