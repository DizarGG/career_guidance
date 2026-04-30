from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.testing.suite.test_reflection import users
from .models import User

class UserRepository:
    def create_user(self,db:Session,username:str,email:str,password:str):
            user = User(
                username=username,
                email=email,
                password=password,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    def read_users(self,db:Session):
            users = db.query(User).all()
            return users

    def read_users_id(self,db:Session,user_id:int):
            user = db.query(User).filter(User.id == user_id).first()
            return user

    def delete_user(self,db:Session,user_id:int):
            user = self.read_users_id(db,user_id)
            if user:
                db.delete(user)
                db.commit()
            return user

