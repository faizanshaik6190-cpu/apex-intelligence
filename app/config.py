from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Configuration
    app_name: str = "Apex Intelligence"
    database_url: str = "sqlite:///./apex_intelligence.db"
    debug: bool = True
    owner_email: str = "owner@apexintelligence.com"
    default_min_price: float = 500.0
    default_max_price: float = 5000.0

    # Google Maps API
    google_maps_api_key: Optional[str] = None

    # Twilio Configuration
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None

    # Email Configuration
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"

    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"

    # Voice Configuration
    voice_enabled: bool = True
    voice_provider: str = "openai"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
