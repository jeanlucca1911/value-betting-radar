from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Value Betting Radar"
    PROJECT_VERSION: str = "0.1.0"
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "value_betting_radar"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = None

    # The Odds API
    THE_ODDS_API_KEY: Optional[str] = None
    
    # Affiliate URLs
    BET365_AFFILIATE_URL: Optional[str] = "https://www.bet365.com"
    WILLIAMHILL_AFFILIATE_URL: Optional[str] = "https://www.williamhill.com"
    UNIBET_AFFILIATE_URL: Optional[str] = "https://www.unibet.com"
    PINNACLE_AFFILIATE_URL: Optional[str] = "https://www.pinnacle.com"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Using SQLite for local development (no Docker required)
        return "sqlite+aiosqlite:///./sql_app.db"

    @property
    def FINAL_REDIS_URL(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    class Config:
        env_file = ".env"

settings = Settings()
