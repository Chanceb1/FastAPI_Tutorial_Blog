from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.models import Blog
from app.database import get_session

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
    responses={404: {"description": "Not found"}},
)

# create a new blog
@router.post("/", response_model=Blog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog, session: Session = Depends(get_session)):
    # We need to exclude id because it's None and SQLModel would try to insert it
    db_blog = Blog.from_orm(blog)
    session.add(db_blog)
    session.commit()
    session.refresh(db_blog)
    return db_blog

# return all blogs
@router.get("/", response_model=list[Blog])
def get_blogs(session: Session = Depends(get_session)):
    blogs = session.exec(select(Blog)).all()
    return blogs

# get blog by id
@router.get("/{blog_id}", response_model=Blog)
def get_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# delete a blog
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return {"message": "Blog deleted successfully"}

# update a blog
@router.put("/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, blog: Blog, session: Session = Depends(get_session)):
    existing_blog = session.get(Blog, blog_id)
    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Update attributes
    blog_data = blog.dict(exclude_unset=True)
    for key, value in blog_data.items():
        setattr(existing_blog, key, value)
    
    session.add(existing_blog)
    session.commit()
    session.refresh(existing_blog)
    return existing_blog