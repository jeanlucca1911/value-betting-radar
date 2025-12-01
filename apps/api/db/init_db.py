from sqlalchemy.ext.asyncio import AsyncSession
from db.session import async_engine
from db.models.user import Base as UserBase
from db.models.bet import Base as BetBase

async def init_db():
    """Initialize database tables"""
    async with async_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(BetBase.metadata.create_all)
    
    print("[OK] Database tables created successfully")

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
