from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from typing import Literal


# SCHEMA -> Pydantic Model -> defines the shape of the request


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass

# Response model schema for Users

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    email: str

    class Config:
        orm_mode = True # pydantic v1
        from_attributes = True # pydantic v2


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Vote(BaseModel):
    post_id: int
    # dir: Literal[0,1]


# Response model schema for Posts
class PostBase(BaseModel):
    title: str
    content: str
    reference: Optional[str] = None
    publish: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True # pydantic v1
        from_attributes = True # pydantic v2

class PostOut(PostBase):
    """
    After using joins this response table will return
    {Post: {}, vote: int }
    """

    post: PostResponse # key as table 1 Post and val is the post class Post
    vote: int

    class Config:
        orm_mode = True # pydantic v1
        from_attributes = True # pydantic v2




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
