from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Admin
from app.schemas import AdminResponse

router = APIRouter(prefix="/admins", tags=["admins"])


@router.get("", response_model=list[AdminResponse])
async def list_admins(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).order_by(Admin.created_at))
    return list(result.scalars().all())
