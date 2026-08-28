from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserLogin, Token
from app.auth.security import create_access_token, verify_password
from app.db.mongo import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = get_database()
    user = await db.users.find_one({"username": credentials.email})
    password_hash = user.get("password_hash", "") if user else ""
    if not user or not password_hash or not verify_password(credentials.password, password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}