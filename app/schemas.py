from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


class ItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class AdminResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
