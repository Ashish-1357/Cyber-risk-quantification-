"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Info
    app_name: str = Field(default="Cyber Risk Quantification Platform", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    environment: str = Field(default="production", alias="ENVIRONMENT")

    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    workers: int = Field(default=4, alias="WORKERS")

    # Security
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    api_key_header: str = Field(default="X-API-Key", alias="API_KEY_HEADER")

    # CORS
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")

    # FAIR Model
    default_simulations: int = Field(default=50000, alias="DEFAULT_SIMULATIONS")
    max_simulations: int = Field(default=100000, alias="MAX_SIMULATIONS")

    # Optimization
    default_budget: float = Field(default=3000000.0, alias="DEFAULT_BUDGET")
    default_staff_capacity: int = Field(default=50, alias="DEFAULT_STAFF_CAPACITY")
    default_risk_appetite: float = Field(default=5000000.0, alias="DEFAULT_RISK_APPETITE")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")

    # Data
    num_assets: int = Field(default=500, alias="NUM_ASSETS")
    num_vulnerabilities_per_asset: int = Field(default=2, alias="NUM_VULNERABILITIES_PER_ASSET")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
