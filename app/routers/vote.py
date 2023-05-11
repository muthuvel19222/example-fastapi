from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, models, schema, oauth2

router= APIRouter(
    prefix="/votes",
    tags=['VOTE']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db:Session=Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{vote.post_id} doesn't exit")
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id == current_user.id)
    found_vote=vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on this post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id, user_id=current_user.id)
        print(f"indise {found_vote} and {vote.dir}")
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote doesn't exit")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted successfully"}
