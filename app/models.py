from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__='posts'
    id = Column(Integer, nullable=False, primary_key=True)
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    published= Column(Boolean, nullable=False, server_default="True")
    created_at= Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)
    owner_id= Column(Integer,ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    owner = relationship('User')


class User(Base):
    __tablename__='users'
    id = Column(Integer, nullable=False, primary_key=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)
    phone_number=Column(String)

class Vote(Base):
    __tablename__='votes'
    user_id= Column(Integer,ForeignKey('users.id', ondelete="CASCADE"),nullable=False,primary_key=True)
    post_id= Column(Integer,ForeignKey('posts.id', ondelete="CASCADE"),nullable=False,primary_key=True)




# from pydantic import BaseModel, validator
# class Vote(BaseModel):
#     post_id: int
#     dir: int
#     @validator('dir')
#     def prevent_zero(cls, v):
#         if v not in (0,1): 
#             raise ValueError('ensure this value is 0 or 1')
#         return v