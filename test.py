from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    ratings: Optional[int] = None

my_posts = [{'title': 'title 1', 'content': 'content 1', 'id': 1}, {'title': 'title 2', 'content': 'content 2', 'id': 2}]

@app.get('/')
def root():
    return {"message": "Welcome to my Api"}

@app.get('/posts/')
def get_all():
    return {'all post': my_posts}

@app.get('/posts/{id}')
def get_post(id:int):
    for post in my_posts:
        if post['id'] == id:
            return {"Post Detail": post}

@app.post('/posts/')
def create_post(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(3, 1000000)
    my_posts.append(post_dict)
    return {'New Post': post_dict}
