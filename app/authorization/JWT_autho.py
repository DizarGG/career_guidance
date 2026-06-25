from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, FastAPI, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from app.datasourse.db_users import engine
from app.datasourse.models import User
from fastapi.security import OAuth2PasswordBearer

JWT_router = APIRouter()

USER_NAME = "admin"
PASSWORD = "123"
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)

    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")

    if username is None:
        raise credentials_exception
    return username


@JWT_router.post("/login")
def login(username: str, password: str):

    # with Session(engine) as session:
    #
    #     user = session.query(User).filter(
    #         username == User.username
    #     ).first()
    #
        if username != USER_NAME:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if password != PASSWORD:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token(
            {"sub": str(username)}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }