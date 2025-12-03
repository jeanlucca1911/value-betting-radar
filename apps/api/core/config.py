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
    POSTGRES_URL: Optional[str] = None
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = None

    # The Odds API
    THE_ODDS_API_KEY: Optional[str] = None
    ODDS_CACHE_MINUTES: int = 15
    
    # Affiliate URLs
    BET365_AFFILIATE_URL: Optional[str] = "https://www.bet365.com"
    WILLIAMHILL_AFFILIATE_URL: Optional[str] = "https://www.williamhill.com"
    UNIBET_AFFILIATE_URL: Optional[str] = "https://www.unibet.com"
    PINNACLE_AFFILIATE_URL: Optional[str] = "https://www.pinnacle.com"

    # Bookmaker Weights (for True Odds Calculation)
    BOOKMAKER_WEIGHTS: dict = {
        "pinnacle": 5.0,
        "betfair": 4.0,
        "betisn": 3.0,
        "bet365": 1.5,
        "williamhill": 1.2,
        "default": 1.0
    }

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Use SQLite for local development if no Postgres URL is provided
        if self.POSTGRES_URL:
            return self.POSTGRES_URL
        # Only use Postgres if explicitly configured
        if self.POSTGRES_SERVER != "localhost" or self.POSTGRES_DB != "value_betting_radar":
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        # Default to SQLite for local dev
        return "sqlite+aiosqlite:///./sql_app.db"

    @property
    def SYNC_SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.POSTGRES_URL:
            return self.POSTGRES_URL.replace("+asyncpg", "")
        if self.POSTGRES_SERVER != "localhost" or self.POSTGRES_DB != "value_betting_radar":
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"

settings = Settings()
