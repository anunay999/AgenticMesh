from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    environment: str
    genai_api_key: str # Default to an empty string if not set

    class Config:
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()