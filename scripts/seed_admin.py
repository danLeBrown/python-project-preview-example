"""
Admin seeder: creates initial admin records in the database.
Run with: python -m scripts.seed_admin
Requires DATABASE_URL in .env (sync URL for create_engine; use postgresql:// for sync).
"""
import asyncio
import os
import sys

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Use DATABASE_URL as-is (async)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/preview_example")

# Default admin to seed if none exist
DEFAULT_ADMINS = [
    {"email": "admin@example.com", "name": "Admin User"},
    {"email": "preview@example.com", "name": "Preview Admin"},
]


async def seed_admins():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Ensure admins table exists (idempotent for preview environments)
    async with engine.begin() as conn:
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))

    async with async_session() as session:
        for admin in DEFAULT_ADMINS:
            result = await session.execute(
                text("SELECT 1 FROM admins WHERE email = :email"),
                {"email": admin["email"]},
            )
            if result.scalar_one_or_none() is None:
                await session.execute(
                    text("INSERT INTO admins (email, name) VALUES (:email, :name)"),
                    admin,
                )
                print(f"Seeded admin: {admin['email']}")
            else:
                print(f"Admin already exists: {admin['email']}")
        await session.commit()

    await engine.dispose()
    print("Admin seeder finished.")


if __name__ == "__main__":
    asyncio.run(seed_admins())
