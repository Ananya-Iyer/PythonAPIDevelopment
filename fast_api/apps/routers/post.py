from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from fastapi import APIRouter
from apps.database import get_db
from apps import models
from apps import schemas
from sqlalchemy.orm import Session
from typing import List
from apps import utils
from apps import oauth2
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
def get_posts(db: Session = Depends(get_db), response_model=List[schemas.PostOut]):
    # posts = db.query(models.Post).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).all()

    """
    cant use return posts

    The issue is that FastAPI does not automatically enforce response models on ORM objects like SQLAlchemy models. 
    When you return db.query(models.Post).all(), it returns SQLAlchemy model instances, which are then directly serialized into 
    JSON, bypassing FastAPIs response model (PostResponse)
    either use:
    return [schemas.PostResponse.model_validate(post) for post in posts]
    return [schemas.PostResponse.from_orm(post) for post in posts]
    after the schemas change and adding PostOut the following return works
    return [{"post": post, "vote": vote} for post, vote in posts]
    """

    return posts


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model=schemas.PostOut):

    # post = db.query(models.Post).filter(models.Post.id == id).first()  # here filter = WHERE clause and first = gets the first instance
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
           models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
           models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found"
                            )

    """
    return [schemas.PostResponse.from_orm(post) for post in posts] 
    or
    return post
    """
    return post    


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    new_post= models.Post(owner_id = current_user.id, **post.dict())
    # or you could also add like this: new_post.owner_id = current_user.id
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # returning the data in case of sqlalchemy

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)  # the first() is not used here because otherwise we cant use .delete attribute
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found"
                            )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"User {id} not Authorized to perform requested action !"
                            )
    post_query.delete(synchronize_session=False)
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), 
                response_model=schemas.PostResponse, current_user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found"
                            )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"User {id} not Authorized to perform requested action !"
                            )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
