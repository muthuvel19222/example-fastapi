from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema, utils
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=["USERS"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
async def user_create(user: schema.UserCreate, db:Session=Depends(get_db)):

    # Hash Password
    hash_password=utils.Hash(user.password)
    user.password=hash_password

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schema.UserResponse)
async def get_user(id: int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")
    return user