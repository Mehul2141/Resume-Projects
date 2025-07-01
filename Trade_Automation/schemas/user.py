from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    mobile: str
    password: str
    role: str = "user"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
