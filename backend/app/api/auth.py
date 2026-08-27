from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserLogin, Token
from app.auth.security import create_access_token, verify_password, get_password_hash

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Mock credentials store for early API route testing
MOCK_USERS_DB = {
    "officer@cybersentinel.gov": {
        "username": "officer@cybersentinel.gov",
        "password_hash": get_password_hash("officer123"),
        "role": "LEA Officer"
    },
    "admin@cybersentinel.gov": {
        "username": "admin@cybersentinel.gov",
        "password_hash": get_password_hash("admin123"),
        "role": "Admin"
    }
}

@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    user = MOCK_USERS_DB.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}