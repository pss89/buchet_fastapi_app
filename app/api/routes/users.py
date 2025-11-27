from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.schemas.user import UserCreate, UserRead, UserPasswordChange
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        return await UserService.register(db, email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[UserRead])
async def list_users(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db_session)):
    return await UserService.get_users(db, limit=limit, offset=offset)

@router.post("/change-password", response_model=UserRead)
async def change_password(
    payload: UserPasswordChange,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        user = await UserService.change_password(
            db,
            email=payload.email,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
        return user
    except ValueError as e:
        # 메시지에 따라 400 / 404 나눠도 됨
        msg = str(e)
        if msg == "User not found":
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)