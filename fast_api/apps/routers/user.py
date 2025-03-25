from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from fastapi import APIRouter
from apps.database import get_db
from apps import models
from apps import schemas
from sqlalchemy.orm import Session
from apps import utils

# uses prefix so that in the app url we dont have to duplicate /users and it will automatically add it
# and any parameter after / will be appended automatically

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # has password retrieved from user.password
    user.password = utils.hashing(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id} was not found"
                            )

    return user
