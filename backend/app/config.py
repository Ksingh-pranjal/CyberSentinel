from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    mongodb_connection_string: str = ""
    mongodb_db_name: str = "cybersentinel_db"
    jwt_secret: str = ""
    ml_service_url: str = "http://localhost:8000"
    backend_port: int = 8001

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

settings = Settings()