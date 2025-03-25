from jose import JWTError
from jose import jwt
from datetime import datetime
from datetime import timedelta
from apps import schemas
from apps import models
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from apps.database import get_db
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expireTime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expireTime})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def _verify_access_token(token: str, credentials_exception):

    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        id = decoded_data.get("user_id") # this key is the same key we passed as data when we created the access token in auth.py

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    pass this as a dependency in any of our path operations. When we do that it is going to take the token from request automatically,
    extract the id for us, verify token is correct by calling _verify_access_token and extract the id
    And if we want to automatically fetch the user from the database and then add it to as a parameter into our path operation function

    Basically whenever we want something that requires user to be logged in this function is called for ex while creating posts, updating posts
    """

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    token = _verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
