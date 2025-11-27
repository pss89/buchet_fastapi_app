from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password
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


    @staticmethod
    async def change_password(
        db: AsyncSession,
        *,
        email: str,
        current_password: str,
        new_password: str,
    ) -> User:
        # 1) 사용자 존재 여부 확인
        user = await UserRepository.get_by_email(db, email)
        if not user:
            raise ValueError("User not found")

        # 2) 현재 비밀번호 검증
        if not verify_password(current_password, user.hashed_password):
            raise ValueError("Current password is incorrect")

        # 3) 새 비밀번호 해시로 변경
        user.hashed_password = hash_password(new_password)

        await db.commit()
        await db.refresh(user)
        return user