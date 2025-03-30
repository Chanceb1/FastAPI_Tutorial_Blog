from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.models import User
from app.database import get_session

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

# get all users
@router.get("/", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# get user by id
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# create a new user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}

# update a user
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session: Session = Depends(get_session)):
    existing_user = session.get(User, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update attributes
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        if key != "id":  # Don't update the ID
            setattr(existing_user, key, value)
    
    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)
    return existing_user