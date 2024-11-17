from .. import models, schema, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
   # For Login users
    
@router.get('/', response_model=list[schema.UserOut])
def test(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts  


@router.get('/{id}', response_model=schema.UserOut)
def get_id(id: int, db: Session = Depends(get_db)):
    posts  = db.query(models.User).filter(models.User.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found')     
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create(user: schema.UserCreate, db: Session = Depends(get_db)):

    #hash password
    hashed_password = utils.hasher(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    

@router.delete('/{id}', response_model=schema.UserOut)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts=  db.query(models.User).filter(models.User.id ==id)
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found') 
    posts.delete(synchronize_session= False)
    
    db.commit()
    #db.refresh()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.UserOut)
def update(post:schema.UserCreate, id: int, db: Session = Depends(get_db)):
    post_query=  db.query(models.User).filter(models.User.id ==id)
    posting= post_query.first()
    if posting == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id {id} was not found') 
    hashed_password = utils.hasher(post.password)
    post.password = hashed_password
    post =post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()    
    return post_query.first()

