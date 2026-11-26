from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "autonomous-support-triage-agent"
    log_level: str = "INFO"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_kb"
    confidence_threshold: float = 0.75

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
