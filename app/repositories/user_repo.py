from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserRepository:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        res = await db.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, *, email: str, hashed_password: str) -> User:
        obj = User(email=email, hashed_password=hashed_password)
        db.add(obj)
        await db.flush()  # INSERT 후 id 채워짐
        return obj

    @staticmethod
    async def list(db: AsyncSession, *, limit: int = 50, offset: int = 0) -> list[User]:
        res = await db.execute(select(User).limit(limit).offset(offset))
        return list(res.scalars())
