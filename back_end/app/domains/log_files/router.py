from fastapi import APIRouter, UploadFile
from app.infrastructure.storage.local_storage import LocalStorage

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile
):
    result = await LocalStorage.upload(file)

    return result