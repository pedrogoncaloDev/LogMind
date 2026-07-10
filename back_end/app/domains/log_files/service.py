from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.infrastructure.storage.local_storage import LocalStorage

MAX_SIZE = 5 * 1024 * 1024

class LogFileService:

	@staticmethod
	async def upload(file: UploadFile):

		LogFileService.validate_file_extension(file)

		content = await file.read()

		LogFileService.validate_file_size(file)

		result = await LocalStorage.upload(
			file=file,
			content=content
		)

		return result

	@staticmethod
	def validate_file_extension(file: UploadFile):
		extension = Path(file.filename).suffix.lower()

		if extension != ".log":
			raise HTTPException(
				status_code=400,
				detail="Apenas arquivos .log são permitidos"
			)

	@staticmethod
	async def validate_file_size(content: bytes):
		if len(content) > MAX_SIZE:
			raise HTTPException(
				status_code=400,
				detail="Arquivo excede 5MB"
			)