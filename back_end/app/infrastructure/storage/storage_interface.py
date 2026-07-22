from abc import ABC, abstractmethod


class StorageInterface(ABC):

    @staticmethod
    @abstractmethod
    async def upload(file, content: bytes) -> dict:
        pass