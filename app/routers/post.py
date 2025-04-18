from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schema, oauth2
from ..database import get_db
from typing import List, Optional


# create router instance
router = APIRouter(
        prefix="/posts",
        tags=["Posts"]
    )



# endpoints using ORM

@router.get('/', response_model=List[schema.PostOut], operation_id="get_all_posts")

def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int=0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = list(map(lambda x : x._mapping, posts))
    return posts

@router.get('/home', response_model=list[schema.PostOut], operation_id="get_user_posts")
def get_user_post(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int=10):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).limit(limit).all()

    
    return posts

@router.get('/{id}', response_model=schema.PostOut, operation_id="get_post_by_id")
def get_posts(id: int, db:Session = Depends(get_db)):
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == (id,))
    post = post_query.first()

    if post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found!"
        )

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query Post
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    # check if post exist
    if post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found!"
                )
    if post.owner_id != current_user.id:
        raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to perform requested action"
            )
    # delete post
    post_query.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schema.Post)
def update_posts(id:int, updated_post: schema.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Get post query object
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # check if post exists
    if post is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found!"
                )

    if post.owner_id != current_user.id:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to perform requested action"

            )
    # update post
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    updated_post = post_query.first()
    return updated_post


# SQL endpoints commands

#@router.get('/', response_model=List[schema.Post])
#def get_posts():
#    cursor.execute("""SELECT * FROM posts""")
#    posts = cursor.fetchall()

#    return posts

#@router.post('/', response_model=schema.Post, status_code=status.HTTP_201_CREATED)
#def create_posts(post: schema.PostBase, current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#    new_post = cursor.fetchone()
#    conn.commit()

#    return new_post

#@router.get('/{id}', response_model=schema.Post)
#def get_post(id:int):
#    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (id,))
#    post = cursor.fetchone()
#    if post == None:
#        raise HTTPException(
#                status_code=status.HTTP_404_NOT_FOUND,
#                detail=f"post wit id: {id} not found"
#                )
#    return post


#@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id: int, current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))

#    conn.commit()
#    if cursor.rowcount == 0:
#        raise HTTPException(
#                status_code=status.HTTP_404_NOT_FOUND,
#                detail=f"post with id {id} not found!"
#                )
#    else:
#        return Response(status_code=status.HTTP_204_NO_CONTENT)


#@router.put('/{id}', response_model=schema.Post)
#def update_post(id: int, post:schema.PostCreate, current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#                   (post.title, post.content, post.published, (id,)))
#    updated_post = cursor.fetchone()
#    conn.commit()
#    if updated_post == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"post of id: {id} does not exist")
#    return updated_post
