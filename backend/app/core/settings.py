# backend/app/core/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "k8s-yaml-analyzer"
    APP_VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    # severity threshold (CI/CLI can use): CRITICAL,HIGH,MEDIUM,LOW
    FAIL_ON_SEVERITY: str = "HIGH"

    class Config:
        env_prefix = "KYA_"

settings = Settings()
