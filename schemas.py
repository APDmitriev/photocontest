from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class PhotoCreate(BaseModel):
    url: str
    name: str
    description: Optional[str] = None

class PhotoResponse(BaseModel):
    id: int
    url: str
    description: Optional[str] = None
    likes: int
    dislikes: int
    owner: UserResponse

    class Config:
        orm_mode = True

class ContestCreate(BaseModel):
    name: str
    description: str

class ContestResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
