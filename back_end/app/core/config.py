from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
# app/core/config.py -> app -> back_end -> LogMind

BACK_END_DIR = Path(__file__).resolve().parents[2]
# app/core/config.py -> app -> back_end

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_HOST: str = "localhost"
    API_URL: str
    SECRET_KEY: str
    STORAGE_LOCAL_PATH: str = "storage/uploads"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

    @property
    def database_url(self):
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )

    @property
    def storage_local_dir(self) -> Path:
        path = Path(self.STORAGE_LOCAL_PATH)
        return path if path.is_absolute() else BACK_END_DIR / path

settings = Settings()