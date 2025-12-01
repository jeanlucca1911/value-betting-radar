from fastapi import FastAPI
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow Vercel frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    from db.redis import redis_client
    try:
        await redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "error"
        
    return {
        "status": "ok", 
        "project": settings.PROJECT_NAME,
        "redis": redis_status
    }

from routers import odds, bets, auth, advanced
app.include_router(odds.router, prefix="/api/v1/odds", tags=["odds"])
app.include_router(bets.router, prefix="/api/v1/bets", tags=["bets"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(advanced.router, prefix="/api/v1/advanced", tags=["advanced"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
