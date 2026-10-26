from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    META_API_KEY: str = ""
    META_BASE_URL: str = "https://api.meta.ai/v1"
    META_MODEL: str = "muse-spark"

    FIREWORKS_API_KEY: str = ""
    FIREWORKS_BASE_URL: str = "https://api.fireworks.ai/inference/v1"
    FIREWORKS_MODEL: str = "accounts/fireworks/models/llama-v3p3-70b-instruct"

    BASETEN_API_KEY: str = ""
    BASETEN_BASE_URL: str = "https://model-xxxx.api.baseten.co/v1"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:5174"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

@lru_cache
def get_settings():
    return Settings()
