from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# ----------------------
# REGISTER USER
# ----------------------
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if email already exists (BEFORE creating anything)
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserOut.model_validate(db_user)

# ----------------------
# LOGIN USER
# ----------------------
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # Get user by email
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    # Check if user exists and password matches
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    # if not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Inactive user"
    #     )

    # Create access token
    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},  # use string ID for JWT
        # expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
