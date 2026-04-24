from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
