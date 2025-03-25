from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from fastapi import APIRouter
from apps.database import get_db
from apps import models
from apps import schemas
from sqlalchemy.orm import Session
from apps import utils
from apps import oauth2


router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {vote.post_id} was not found"
                            )

    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.owner_id==current_user.id)
    found_vote = vote_query.first()

    if found_vote:
        # post in state: liked or upvoted
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Successfully deleted vote"}

    # post in state: downvoted or unliked
    vote = models.Vote(post_id=vote.post_id, owner_id=current_user.id)
    db.add(vote)
    db.commit()
    return {"Message": "Successfully added vote"}
