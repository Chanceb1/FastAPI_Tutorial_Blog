from fastapi import APIRouter, status, HTTPException, Depends
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.schemas import login as login_schema
from sqlalchemy.orm import Session
from app.utils.user import get_user_by_email
from app.security import Hash


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
def login_user(request: login_schema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create an instance of Hash
    hash_util = Hash()
    
    if not hash_util.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # if request.password != user.password:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    # Generate JWT token here (not implemented in this snippet)
    # token = create_jwt_token(user)

    return {"access_token": user.email, "token_type": "bearer"}    