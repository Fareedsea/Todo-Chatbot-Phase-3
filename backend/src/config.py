"""
Application configuration loaded from environment variables.

Uses pydantic-settings for type-safe configuration with validation.
All secrets MUST be provided via environment variables (never hardcoded).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Required Variables:
    - NEON_DB_URL: PostgreSQL connection string with SSL
    - BETTER_AUTH_SECRET: JWT signature verification secret (32+ chars)
    - FRONTEND_URL: Frontend origin for CORS allow-list

    Optional Variables:
    - ENVIRONMENT: Runtime environment (default: development)
    - PORT: Server port (default: 8000)
    - LOG_LEVEL: Logging verbosity (default: INFO)
    - COHERE_API_KEY: Cohere API key for AI chatbot (Phase III)
    - COHERE_MODEL: Cohere model name (default: command-r-plus)
    """

    # Database Configuration (REQUIRED)
    neon_db_url: str

    # Authentication Configuration (REQUIRED)
    better_auth_secret: str

    # CORS Configuration (REQUIRED)
    frontend_url: str

    # Application Configuration (OPTIONAL)
    environment: str = "development"
    port: int = 8000
    log_level: str = "INFO"

    # JWT Configuration
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # AI Chatbot Configuration (Phase III)
    cohere_api_key: str = ""
    cohere_model: str = "command-r-plus"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore unknown env vars
    )

    @property
    def database_url(self) -> str:
        """Alias for neon_db_url to match SQLModel expectations."""
        return self.neon_db_url

    @property
    def secret_key(self) -> str:
        """Alias for better_auth_secret for internal use."""
        return self.better_auth_secret


# Global settings instance (loaded once on import)
settings = Settings()
