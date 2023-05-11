import time
from fastapi import Body, FastAPI , Response , status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


app=FastAPI()

# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool = True
#     rating: Optional[int] = None
class Post(BaseModel):
    title:str
    content:str
    published:bool = True
   

while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='admin',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database was connected sucessfully")
        break
    except Exception as e:
        print(f"Database connection was failed due to {e}")
        time.sleep(4)


my_post=[{"title":"title of post 1", "content":"content of post 1","id":1},{"title":"favorite foods", "content":"I like pizza very much","id":2},{"title": "FlaskApi",
        "content": "Bit older framework","published": False,"rating": 3,"id": 43613}]


# @app.get("/login")
# async def rot():
#     return {"message":"hello"}

# @app.post("/post")
# async def post(payload: dict=Body(...)):
#     return {"data":f"title:{payload['title']}, content:{payload['content']}"}
 
# @app.post("/baseclass")
# async def post(new_post:Post):
#     print(new_post)
#     print(new_post.dict())
#     return {"data":new_post}


def find_post(id):
    for p in my_post:
        if p['id']==id:
            return p

def find_inex_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
            

# @app.get("/posts")
# async def get_posts():
#     return {"data":my_post}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data":posts}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# async def create_post(post: Post):
#     post_dict=post.dict()
#     post_dict['id']=randrange(0,100000)
#     my_post.append(post_dict)
#     return {"data":post_dict}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    new_posts=cursor.fetchone()
    conn.commit()
    return {"data":new_posts}

@app.get("/posts/latest")
async def get_post_latest():
    post=my_post[len(my_post)-1]
    return {"post_details":post}

# @app.get("/posts/{id}")
# async def get_post(id: int, response : Response):
#     post=find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This id:{id} or data is not exist")
#         # response.status_code = status.HTTP_400_BAD_REQUEST
#         # return {"message":f"This id:{id} or data is not exist"}
#     return {"post_details":post}

@app.get("/posts/{id}")
async def get_post(id: int, response : Response):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""",(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {"message":f"This id:{id} or data is not exist"}
    return {"post_details":post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#     index=find_inex_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This id:{id} or data is not exist")
#     my_post.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""",(str(id)))
    delete_post=cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT)
# async def update_post(id: int,post:Post):
#     index=find_inex_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")
#     update_post=post.dict()
#     update_post["id"]=id
#     my_post[index]=update_post
#     return {"post_details":post}

@app.put("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT)
async def update_post(id: int,post:Post):
    update_post=find_inex_post(id)
    cursor.execute("""UPDATE posts SET title=%s, content=%s , published=%s WHERE id = (%s) RETURNING *""",(post.title,post.content,post.published,str(id)))
    update_post=cursor.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This id:{id} or data is not exist")

    return {"post_details":update_post}