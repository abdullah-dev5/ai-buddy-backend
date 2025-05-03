from fastapi import APIRouter
from app.services.export import generate_txt

router = APIRouter()

@router.get("/")
def export_summary(summary: str):
    filepath = generate_txt(summary)
    return {"file_url": f"/files/{filepath}"}
