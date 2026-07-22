from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.infrastructure.storage.local_storage import LocalStorage
from app.domains.users.model import User
from . import repository as log_file_repository

MAX_SIZE = 5 * 1024 * 1024

class LogFileService:

	@staticmethod
	async def upload(file: UploadFile, current_user: User):

		LogFileService.validate_file_extension(file)

		content = await file.read()

		LogFileService.validate_file_size(content)

		storage_result = await LocalStorage.upload(
			file=file,
			content=content
		)

		return log_file_repository.create_log_file(
			user_id=current_user.id,
			original_filename=storage_result["original_filename"],
			stored_filename=storage_result["stored_filename"],
			file_size=storage_result["file_size"],
		)


	@staticmethod
	def validate_file_extension(file: UploadFile):
		extension = Path(file.filename).suffix.lower()

		if extension != ".log":
			raise HTTPException(
				status_code=400,
				detail="Apenas arquivos .log são permitidos"
			)


	@staticmethod
	def validate_file_size(content: bytes):
		if len(content) > MAX_SIZE:
			raise HTTPException(
				status_code=400,
				detail="Arquivo excede 5MB"
			)