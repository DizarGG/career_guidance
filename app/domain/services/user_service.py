from sqlalchemy.orm import Session,sessionmaker
from app.datasourse.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, db:Session,username:str, email:str,password: str):
        return self.repo.create_user(db,username,email,password)

    def read_users(self, db:Session):
        return self.repo.read_users(db)

    def read_users_id(self,db:Session,user_id:int):
        return self.repo.read_users_id(db, user_id)

    def delete_user(self, db: Session, user_id: int):
        return self.repo.delete_user(db, user_id)
