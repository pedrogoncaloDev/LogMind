from app.infrastructure.storage.storage_interface import StorageInterface


class LocalStorage(StorageInterface):
	
	@staticmethod
	async def upload(self, file, content):
		# Implement local storage upload logic here
		pass