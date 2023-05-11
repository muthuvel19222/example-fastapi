from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)   
app.include_router(user.router)   
app.include_router(auth.router)   
app.include_router(vote.router)   


from jose import jwt


SECRET_KEY = "mysecretkey"
SECRET_KEY_REFRESH = "mysecretksdasdasdaey"
ALGORITHM = "HS256"

@app.get("/")
async def create_jwt():
    to_encode = {"sub": "123"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encoded_refresh = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return {"token": encoded_jwt, "refresh_token":encoded_refresh, "message":"Hello World"}