from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    BITRIX_URL: str = Field(..., env="BITRIX_URL")
    DEBUG: bool = Field(False, env="DEBUG")
    APP_HOST: str = Field("0.0.0.0", env="APP_HOST")
    APP_PORT: int = Field(8000, env="APP_PORT")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
