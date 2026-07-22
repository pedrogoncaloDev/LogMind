import uuid
from pathlib import Path

from app.core.config import settings
from app.infrastructure.storage.storage_interface import StorageInterface


class LocalStorage(StorageInterface):

	@staticmethod
	async def upload(file, content: bytes) -> dict:
		storage_dir = settings.storage_local_dir
		storage_dir.mkdir(parents=True, exist_ok=True)

		extension = Path(file.filename).suffix
		stored_filename = f"{uuid.uuid4()}{extension}"
		destination = storage_dir / stored_filename

		destination.write_bytes(content)

		return {
			"original_filename": file.filename,
			"stored_filename": stored_filename,
			"file_size": len(content),
		}