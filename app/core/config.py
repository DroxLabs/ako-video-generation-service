from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "RunwayML FastAPI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    RUNWAY_API_KEY: str
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings() 