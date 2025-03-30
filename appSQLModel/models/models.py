from typing import Optional
from sqlmodel import Field, SQLModel

class Blog(SQLModel, table=True):
    __tablename__ = "blogs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: Optional[bool] = Field(default=True)
    
    class Config:
        arbitrary_types_allowed = True


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    
    class Config:
        arbitrary_types_allowed = True