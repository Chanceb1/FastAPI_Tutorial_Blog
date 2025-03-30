from pydantic import BaseModel, Field

class Blog(BaseModel):
    title: str
    content: str
    published: bool | None


class User(BaseModel):
    id: int | None = Field(default=None, title="User ID")
    name: str = Field(..., title="User Name")
    email: str = Field(..., title="User Email")
    password: str = Field(..., title="User Password")
