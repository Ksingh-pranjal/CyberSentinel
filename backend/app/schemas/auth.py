from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    name: str
    role: str

class UserDocument(BaseModel):
    username: str
    name: str
    role: str
    password_hash: str