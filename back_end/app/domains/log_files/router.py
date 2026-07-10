from pathlib import Path
from fastapi import APIRouter, UploadFile
from app.infrastructure.storage.local_storage import LocalStorage
from fastapi import HTTPException, Depends

router = APIRouter()

MAX_SIZE = 5 * 1024 * 1024



@router.post("/upload")
async def upload_file(
    file: UploadFile
):
	try:
		# Validate JWT Token
		current_user = Depends(get_current_user)
		
		validate_file_extension()		
		validate_file_size()

		result = await LocalStorage.upload(file)

		return result
	except Exception as e:
		raise e