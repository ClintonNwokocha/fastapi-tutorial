from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db

# Create a router instance
router = APIRouter(
        prefix="/users",
        tags=["Users"]
    )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db:Session = Depends(get_db)):
    
    # Hash the password for security
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # New user instance using the data from the request
    new_user = models.User(**user.dict())

    # Adding it to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schema.UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):

    # Query the database for a user with the given ID
    user = db.query(models.User).filter(models.User.id==id).first()

    # id user doesn't exist, raise 404 error
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} not found!"
                )

    return user

