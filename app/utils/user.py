from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.models import User



# CRUD operations for User models


# Get all users from the database
def get_all_users(db: Session):
    users = db.query().all()
    return users


# get a specific user by ID
def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()  # Get a specific user by ID
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user