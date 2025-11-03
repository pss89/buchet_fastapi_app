from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password
from app.models.user import User

class UserService:
    @staticmethod
    async def register(db: AsyncSession, *, email: str, password: str) -> User:
        if await UserRepository.get_by_email(db, email):
            raise ValueError("Email already registered")
        user = await UserRepository.create(
            db, email=email, hashed_password=hash_password(password)
        )
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_users(db: AsyncSession, *, limit: int = 50, offset: int = 0) -> list[User]:
        return await UserRepository.list(db, limit=limit, offset=offset)
