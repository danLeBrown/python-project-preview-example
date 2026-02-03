from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Item
from app.redis_client import get_redis
from app.schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).order_by(Item.created_at.desc()))
    return list(result.scalars().all())


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(body: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = Item(title=body.title, description=body.description)
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/stats/requests")
async def request_stats():
    """Demonstrates Redis: returns a simple request counter."""
    redis_client = await get_redis()
    count = await redis_client.incr("api:request_count")
    return {"request_count": count}
