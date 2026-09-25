from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    # App Configuration
    app_name: str = "Apex Intelligence"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./apex_intelligence.db")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    owner_email: str = "owner@apexintelligence.com"
    default_min_price: float = 500.0
    default_max_price: float = 5000.0

    # Google Maps API
    google_maps_api_key: Optional[str] = os.getenv("GOOGLE_MAPS_API_KEY")

    # Twilio Configuration
    twilio_account_sid: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = os.getenv("TWILIO_PHONE_NUMBER")

    # Email Configuration
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")

    # Redis Configuration
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # OpenAI Configuration
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # Voice Configuration
    voice_enabled: bool = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    voice_provider: str = os.getenv("VOICE_PROVIDER", "openai")

    # Server Configuration
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    server_workers: int = int(os.getenv("SERVER_WORKERS", "4"))

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
