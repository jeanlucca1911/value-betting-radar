from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# Get the directory where this config file is located (apps/api/core)
CORE_DIR = Path(__file__).parent
API_DIR = CORE_DIR.parent  # apps/api
ENV_FILE = API_DIR / ".env"

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
    ODDS_CACHE_MINUTES: int = 15  # Cache for 15 mins as requested
    
    # Affiliate URLs
    BET365_AFFILIATE_URL: Optional[str] = "https://www.bet365.com"
    WILLIAMHILL_AFFILIATE_URL: Optional[str] = "https://www.williamhill.com"
    UNIBET_AFFILIATE_URL: Optional[str] = "https://www.unibet.com"
    PINNACLE_AFFILIATE_URL: Optional[str] = "https://www.pinnacle.com"

    # Bookmaker Weights (for True Odds Calculation)
    # Higher weight = sharper bookmaker (more accurate lines)
    BOOKMAKER_WEIGHTS: dict = {
        "pinnacle": 5.0,        # Sharpest book worldwide
        "betfair": 4.0,         # Exchange, very sharp
        "betisn": 3.0,
        "draftkings": 3.5,      # Sharp for US sports (NBA, NFL)
        "fanduel": 3.0,         # Sharp for US sports
        "bet365": 1.5,
        "williamhill": 1.2,
        "mybookie": 0.8,        # Often soft/recreational
        "bovada": 1.0,
        "caesars": 1.3,
        "betmgm": 1.3,
        "betrivers": 1.2,
        "lowvig": 2.0,          # Low-vig books tend to be sharper
        "default": 1.0
    }
    
    # Sport-Specific Edge Thresholds
    # More efficient markets (NBA) need lower thresholds
    EDGE_THRESHOLDS: dict = {
        "basketball_nba": 0.005,      # 0.5% - very efficient market
        "americanfootball_nfl": 0.008,  # 0.8%
        "icehockey_nhl": 0.008,       # 0.8%
        "baseball_mlb": 0.010,        # 1.0%
        "soccer_epl": 0.010,          # 1.0%
        "soccer_uefa_champions_league": 0.010,
        "default": 0.010              # 1.0% for other sports
    }

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Use SQLite for local development if no Postgres URL is provided
        if self.POSTGRES_URL:
            if self.POSTGRES_URL.startswith("postgresql://"):
                return self.POSTGRES_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
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
        env_file = str(ENV_FILE)  # Use absolute path to .env
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()
