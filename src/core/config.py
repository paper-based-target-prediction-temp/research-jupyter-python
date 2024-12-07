from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_DB_URI: str = Field(..., description="MongoDB URI")
    MONGO_DB_NAME: str = Field(..., description="MongoDB DB Name")
    MAX_CONNECTIONS_COUNT: int = Field(default=10, description="Max Connections Count")
    MIN_CONNECTIONS_COUNT: int = Field(default=5, description="Min Connections Count")
    SERVER_SELECTION_TIMEOUT_MS: int = Field(
        default=20000, description="Server Selection Timeout (ms)"
    )

    # Pubmed API Settings
    PUBMED_API_KEY: str = Field(..., description="Pubmed API Key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
