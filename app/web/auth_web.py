from fastapi import HTTPException, FastAPI, APIRouter
from typing import List
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import select
from app.datasourse.db_users import engine
from app.domain.models.crt_usr import UserResponse
from app.domain.models.crt_usr import UserCreate
from app.datasourse.user_repository import User

router =  APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user_in: UserCreate):
    with Session(engine) as session:
        user = User(
            username=user_in.username,
            email=user_in.email,
            password=user_in.password,
            is_active=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.get("/users", response_model=List[UserResponse])
def read_users():
    with Session(engine) as session:
        users = session.query(User).all()
        return users


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": "User deleted"}