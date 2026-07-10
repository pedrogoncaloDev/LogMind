from abc import ABC, abstractmethod

class StorageInterface(ABC):
    
    @abstractmethod
    async def upload(self, file):
        pass