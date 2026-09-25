from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Apex Intelligence"
    database_url: str = "sqlite:///./apex_intelligence.db"
    debug: bool = True
    owner_email: str = "owner@apexintelligence.com"
    default_min_price: float = 500.0
    default_max_price: float = 5000.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
