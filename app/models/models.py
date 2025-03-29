from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base  # Change from 'base' to 'Base'

class Blog(Base):  # Change from 'base' to 'Base'
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)