import asyncio
import os
import sys
import time
from app.config import HUGGINGFACE_API_TOKEN, TRANSCRIPTION_MODEL, CHUNK_DURATION, CHUNK_DELAY
from app.utils.whisper_api import transcribe_chunk, check_model_status
from app.utils.audio_chunker import split_audio, clean_up_chunks

def get_unique_filename(base_path: str) -> str:
    """Generate a unique filename by appending numbers if file exists"""
    counter = 1
    name, ext = os.path.splitext(base_path)
    while os.path.exists(base_path):
        base_path = f"{name}_{counter}{ext}"
        counter += 1
    return base_path

async def process_audio(file_path: str):
    """Complete transcription pipeline"""
    print(f"\n🔊 Processing: {file_path}")
    print(f"📏 Size: {os.path.getsize(file_path)/1024/1024:.2f}MB")

    # Verify model access
    if not await check_model_status():
        return False

    chunks = []
    try:
        # Split and process
        chunks = split_audio(file_path, CHUNK_DURATION)
        full_transcript = []
        
        for i, chunk in enumerate(chunks):
            print(f"\n🔄 Chunk {i+1}/{len(chunks)}")
            
            if i > 0 and CHUNK_DELAY > 0:
                print(f"⏳ Waiting {CHUNK_DELAY}s...")
                await asyncio.sleep(CHUNK_DELAY)
            
            result = await transcribe_chunk(chunk)
            if result and 'text' in result:
                # Print individual chunk transcript
                print(f"\n📝 Chunk {i+1} Transcript:")
                print("-" * 40)
                print(result['text'])
                print("-" * 40)
                
                full_transcript.append(result['text'])
                print(f"✅ Chars: {len(result['text'])}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown')}")

        # Save results with unique filename
        if full_transcript:
            base_output = f"{os.path.splitext(file_path)[0]}_transcript.txt"
            output_path = get_unique_filename(base_output)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(full_transcript))
            
            print(f"\n🎉 Full transcript saved to {output_path}")
            return True

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
    finally:
        clean_up_chunks(chunks)
    
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(process_audio(sys.argv[1]))
    else:
        print("Usage: python test_audio_transcription.py audio.wav")