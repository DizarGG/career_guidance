from fastapi import HTTPException, FastAPI, APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from app.datasourse.db_users import engine
from app.domain.models.crt_usr import UserResponse
from app.domain.models.crt_usr import UserCreate
from app.datasourse.user_repository import User
from app.authorization.JWT_autho import get_current_user

router = APIRouter()

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

@router.get("/protected/profile")
def get_profile(current_user: str = Depends(get_current_user)):
    return {
        "message": f"Welcome, {current_user}!",
        "user": current_user,
        "status": "authorized"
    }

@router.get("/protected/secret-data")
def get_secret_data(current_user: str = Depends(get_current_user)):
    return {
        "message": "This is secret data!",
        "data": {
            "secret_key": "12345-SECRET-67890",
            "top_secret_info": "Only for authorized users"
        },
        "accessed_by": current_user
    }
