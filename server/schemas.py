from pydantic import BaseModel

class Message(BaseModel):
    text: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    is_active: bool

    class Config:
        from_attributes = True