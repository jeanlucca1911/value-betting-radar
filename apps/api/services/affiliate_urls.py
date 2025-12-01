"""
Affiliate URL mapping service.
Maps bookmaker names to their configured affiliate URLs.
"""
from core.config import settings
from typing import Optional

AFFILIATE_URL_MAP = {
    "bet365": settings.BET365_AFFILIATE_URL,
    "williamhill": settings.WILLIAMHILL_AFFILIATE_URL,
    "william hill": settings.WILLIAMHILL_AFFILIATE_URL,
    "unibet": settings.UNIBET_AFFILIATE_URL,
    "pinnacle": settings.PINNACLE_AFFILIATE_URL,
}

def get_affiliate_url(bookmaker_name: str) -> Optional[str]:
    """
    Get the affiliate URL for a given bookmaker.
    Falls back to a default format if not configured.
    """
    # Normalize bookmaker name
    normalized = bookmaker_name.lower().replace(" ", "")
    
    # Try exact match first
    if normalized in AFFILIATE_URL_MAP:
        return AFFILIATE_URL_MAP[normalized]
    
    # Try with spaces
    normalized_with_space = bookmaker_name.lower()
    if normalized_with_space in AFFILIATE_URL_MAP:
        return AFFILIATE_URL_MAP[normalized_with_space]
    
    # Fallback: generate a generic URL
    clean_name = bookmaker_name.lower().replace(" ", "")
    return f"https://www.{clean_name}.com/register?ref=valuebettingradar"
