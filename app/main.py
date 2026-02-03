from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, Base
from app.models import Admin, Item
from app.redis_client import close_redis, get_redis
from app.routers import admins, health, items


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await close_redis()


app = FastAPI(
    title="Preview Example API",
    description="Example FastAPI app for preview tool: Postgres, Redis, health check.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(items.router)
app.include_router(admins.router)


@app.get("/")
async def root():
    return {"message": "Preview Example API", "docs": "/docs"}
