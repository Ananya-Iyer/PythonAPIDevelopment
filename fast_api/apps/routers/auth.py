from fastapi import HTTPException
from fastapi import Depends
from fastapi import APIRouter
from fastapi import Response
from fastapi import status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from apps.database import get_db
from apps import schemas
from apps import utils
from apps import models
from apps import oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm returns username and password only by default whether u put username or email in the login page
    # hence we will use user_credentials.username instead of user_credentials.email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Not Found")

    isEqual = utils.verify(user_credentials.password, user.password)

    if not isEqual:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
