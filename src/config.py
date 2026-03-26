from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# определяем абсолютный путь до корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DB_NAME: str
    # pathlib позволяет формировать путь
    # с помощью оператора "/", аналогично os.path.join()
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env") # extra="ignore"

settings = Settings()