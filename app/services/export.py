import uuid

def generate_txt(content: str) -> str:
    filename = f"{uuid.uuid4()}.txt"
    with open(f"generated/{filename}", "w", encoding="utf-8") as f:
        f.write(content)
    return filename
