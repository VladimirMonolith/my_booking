from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, Request, status
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    NotAuthUserException,
    TokenExpireException,
    TokenInvalidDataException,
    TokenInvalidException
)
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get('my_booking_access_token')
    if not token:
        raise NotAuthUserException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise TokenInvalidException
    expire = payload.get('exp')
    if (not expire) or int(expire) < datetime.utcnow().timestamp(): 
        raise TokenExpireException
    user_id = payload.get('sub')
    if not user_id:
        raise TokenInvalidDataException
    return await UserDAO.get_object(id=int(user_id))
