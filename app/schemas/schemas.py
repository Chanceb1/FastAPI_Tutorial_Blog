from pydantic import BaseModel, Field

class Blog(BaseModel):
    title: str
    content: str
    published: bool | None

