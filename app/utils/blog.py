from sqlalchemy.orm import Session
from ..models.models import Blog

# CRUD operations for Blog models


# Get all blogs from the database
def get_all_blogs(db: Session):
    blogs = db.query(Blog).all()
    return blogs


def get_blog_by_id(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()  # Get a specific blog by ID
    return blog
