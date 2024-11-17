from .. import models, schema, utils
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    prefix="/sql",  
    tags=["sql"]
)
@router.get("/{id}", response_model=schema.Post)
async def root(id: int):   
    # using python
    #result = [k for k in my_post if k['id'] ==id]
    #if not result:
     #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      #  detail=f'post with id {id} was not found')

      #using Sql
    
    cursor.execute(""" select * from posts where id =  %s """, (str(id),))
    post  =  cursor.fetchone()  
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found')                             
    return post   



@router.get("/", response_model=list[schema.Post])
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


@router.post("/sql1", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(payload: dict = Body(...)):
    print(payload)
    return payload

# title : str, content: str, category:str, published: False
@router.post("/", status_code=status.HTTP_201_CREATED)
def Post(post: schema.PostCreate):
    #using python
    #post_dict = post.model_dump()
    #post_dict['id'] = randrange(3, 10)
    #my_post.append(post_dict)

    #using sql
    cursor.execute(""" insert into posts (title, content, published) values ( %s, %s, %s) returning * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


#Deleting a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #using sql
    cursor.execute(""" delete from posts where id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
   
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found')
    
    #using python
 #answer = del_fun(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




#update post
@router.put("/{id}", response_model=schema.Post) 
def update_post(id: int,  post: schema.PostCreate):
    #using sql
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning * """, 
                   (post.title, post.content, post.published, str(id),))
    new_post = cursor.fetchone()
    conn.commit()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found') 
   
    #using python
    #ans= del_fun(id)
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_post.pop(ans)
    #my_post.append(post_dict)    
    return new_post