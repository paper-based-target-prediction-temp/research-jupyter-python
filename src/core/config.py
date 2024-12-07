from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_DB_URI: str = Field(..., description="MongoDB URI")
    MONGO_DB_NAME: str = Field(..., description="MongoDB DB Name")

    # Pubmed API Settings
    PUBMED_API_KEY: str = Field(..., description="Pubmed API Key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
