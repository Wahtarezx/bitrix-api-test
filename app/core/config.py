import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BITRIX_URL: str = os.getenv("BITRIX_URL")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
