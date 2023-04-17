from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """Создает хеш пользовательского пароля."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Верифицирует пользовательский пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Cоздает токен доступа."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)  # minutes=60
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    """Аутентифицирует пользователя."""
    user = await UserDAO.get_object(email=email)

    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
