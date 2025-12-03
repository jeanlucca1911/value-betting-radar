print("Loading main.py...")
from fastapi import FastAPI
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://valuebettingradar.com",
        "https://www.valuebettingradar.com",
        "https://value-betting-radar.vercel.app",
        "https://value-betting-radar-git-master-jeanlucca1911s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    print("Starting up... Initializing database...")
    try:
        from db.session import async_engine, Base
        # Import models to ensure they are registered with Base
        from db.models.user import User
        from db.models.bet import Bet
        from db.models.historical import HistoricalMatch, HistoricalOdds
        
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")
        print("Continuing anyway - will use mock data")

@app.get("/")
async def root():
    return {"message": "Value Betting Radar API is running"}

@app.get("/health")
@app.get("/api/v1/health")
async def health_check():
    # Simple health check that doesn't depend on external services
    return {
        "status": "ok", 
        "project": settings.PROJECT_NAME
    }

from routers import odds, bets, auth, advanced
app.include_router(odds.router, prefix="/api/v1/odds", tags=["odds"])
app.include_router(bets.router, prefix="/api/v1/bets", tags=["bets"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(advanced.router, prefix="/api/v1/advanced", tags=["advanced"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
