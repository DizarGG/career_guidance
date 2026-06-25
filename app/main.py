from fastapi import FastAPI
from app.datasourse.db_users import Base,engine
from app.web.auth_web import router
from app.authorization.JWT_autho import JWT_router
from app.authorization.Basic_autho import Basic_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
#  app.include_router(Basic_router)
app.include_router(JWT_router)