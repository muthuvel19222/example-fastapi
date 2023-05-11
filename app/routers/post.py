from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse



router=APIRouter(
    prefix="/posts",
    tags=["POST"]
)


# select users.id as users, count(posts.id) as post from posts RIGHT JOIN users ON posts.owner_id = users.id group by users.id;
# select posts.id as posts, count(votes.post_id) from posts left join votes on posts.id = votes.post_id group by posts.id;




def serialize_post(post):
    serialized_post = jsonable_encoder(post)
    # Perform any additional modifications to the serialized post if needed
    return serialized_post

# @router.get("/")
@router.get("/",  response_model=List[schema.PostOut])
async def get_posts(db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search:Optional[str]=""):
    # posts=db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # result=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # result=db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # serialized_result = jsonable_encoder(result)
    # # print("___________________________",serialized_result)
    # return JSONResponse(content=serialized_result)
    # results = list ( map (lambda x : x._mapping, results) )
    return result


# for those of you who are still getting an error at 10:22:17 like:
# TypeError('cannot convert dictionary update sequence element #0 to a sequence')
# try to add this line of code before returning results:
# results = list ( map (lambda x : x._mapping, results) )
# When querying the db with two arguments in the .query method, sqlalchemy returns a list of sqlalchemy.engine.row.Row objects. As far as I have acknowledged from the documentation:
# "Changed in version 1.4:
# Renamed RowProxy to .Row. .Row is no longer a "proxy" object in that it contains the final form of data within it, and now acts mostly like a named tuple. Mapping-like functionality is moved to the .Row._mapping attribute, but will remain available in SQLAlchemy 1.x ... "
# So, in my understanding, we are not allowed to retrieve the jsonized data directly from the query anymore; the ._mapping method takes care of building the dict structure with "Post" and "votes" keys, and using map does this for each .Row element in the list; we then convert map to a list to be able to return it. 
# Please feel free to correct me if I'm wrong, or if you have any better workaround.


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
async def create_post(post: schema.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.dict()) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schema.PostOut)
async def get_post(id: int, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # post=db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")
    
    if post.owner_id != int(current_user.id) : # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT, response_model=schema.Post)
async def update_post(id: int, updated_post:schema.PostCreate, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")


    if post.owner_id != int(current_user.id) : # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.update(dict(updated_post), synchronize_session=False) # type: ignore
    db.commit()
    return post_query.first()
