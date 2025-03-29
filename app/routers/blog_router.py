from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import Blog as BlogModel
from app.schemas.schemas import Blog as BlogSchema
from app.database import SessionLocal

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
    responses={404: {"description": "Not found"}},
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create a new blog
@router.post("/", response_model=BlogSchema, status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(
        title=blog.title,
        content=blog.content,
        published=blog.published if blog.published is not None else True
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


## return all blogs
@router.get("/", response_model=list[BlogSchema])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


# get blog by id
@router.get("/{blog_id}", response_model=BlogSchema)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# delete a blog
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}


# update a blog
@router.put("/{blog_id}", response_model=BlogSchema)
def update_blog(blog_id: int, blog: BlogSchema, db: Session = Depends(get_db)):
    existing_blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    existing_blog.published = blog.published if blog.published is not None else True
    
    db.commit()
    db.refresh(existing_blog)
    return existing_blog