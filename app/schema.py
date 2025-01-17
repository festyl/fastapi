from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        #orm_mode  = True
        from_attributes= True

class PostCreate(PostBase):
       pass
 

class Post(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserOut
    

    class Config:
        #orm_mode  = True
        from_attributes= True

class PostVote(BaseModel):
    post:Post
    likes:int

    class Config:
        #orm_mode  = True
        from_attributes= True



class UserBase(BaseModel):
    email: EmailStr
    password: str
      


class UserCreate(UserBase):
    pass





class UserLogin(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir :  conint(lt = 2, ge = 0) # type: ignore
