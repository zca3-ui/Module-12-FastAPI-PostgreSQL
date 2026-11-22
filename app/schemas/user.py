
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Schema for registering a new user
class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )


# Schema for logging in an existing user
class UserLogin(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )


# Schema for returning public user information
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
