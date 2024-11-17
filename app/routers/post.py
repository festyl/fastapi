
from typing import List, Optional

from sqlalchemy import func
from . . import models, schema, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#using orm
#@router.get('/', response_model=list[schema.Post])
@router.get('/')
def test(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
         limit: int=20, skip: int=0, search: Optional[str] = ""):

    """ restrict post to users
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    """
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(
     #    limit).offset(skip).all()   # make all post public

    
    posting  = db.query(models.Post,func.count(models.Vote.post_id).label("Likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(
          limit).offset(skip).all() 
    
    posts_new : List[schema.PostVote]= [{"Post": post, "Likes": votes}
             for post, votes in posting]

    return posts_new 
     




@router.get('/{id}')
def get_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # posts  = db.query(models.Post).filter(models.Post.id == id).first()

   
    posting  = db.query(models.Post,func.count(models.Vote.post_id).label("Likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found')
    
    print(posting)
    post, Likes = posting

  
    return {"Post": post, "Likes": Likes}



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # posts = models.Post(title=post.title, content=post.content, published= post.published) or
    print(current_user.email)
    posts = models.Post(owner_id =current_user.id, **post.model_dump()) 
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

    

@router.delete('/{id}', response_model=schema.Post)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query =  db.query(models.Post).filter(models.Post.id ==id)

    post = post_query.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found') 
    post_query.delete(synchronize_session= False)
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform this action ")
    
    db.commit()
    #db.refresh()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.Post)
def update(posts:schema.PostCreate, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query=  db.query(models.Post).filter(models.Post.id ==id)
    post= post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found') 
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform this action ")
    
    post_query.update(posts.model_dump(), synchronize_session=False)
    db.commit()    
    return post_query.first()


