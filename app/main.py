from fastapi import FastAPI
from app.datasourse.db_users import Base,engine
from app.web.auth_web import router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
