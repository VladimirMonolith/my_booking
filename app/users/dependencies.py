from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.exceptions import (
    NotAuthUserException,
    TokenExpireException,
    TokenInvalidDataException,
    TokenInvalidException
)
from app.users.dao import UserDAO


def get_token(request: Request):
    """Добавляет токен доступа в куки."""
    token = request.cookies.get('my_booking_access_token')
    if not token:
        raise NotAuthUserException
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Позволяет получить текущего пользователя."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpireException
    except JWTError:
        raise TokenInvalidException
    user_id = payload.get('sub')
    if not user_id:
        raise TokenInvalidDataException
    return await UserDAO.get_object(id=int(user_id))
