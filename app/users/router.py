from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    IncorrectUserDataException,
    UserAlreadyExistsException
)
from app.users.auth import get_password_hash
from app.users.dependencies import get_current_user
from app.users.models import User

from .auth import authenticate_user, create_access_token
from .dao import UserDAO
from .schemas import UserAuth, UserRead

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/register')
async def register_user(user_data: UserAuth):
    """Регистрирует пользователя."""
    user = await UserDAO.get_object(email=user_data.email)

    if user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add_object(
        email=user_data.email, hashed_password=hashed_password
    )
    return 'Вы успешно зарегистрировались.'


@router.post('/login')
async def login_user(response: Response, user_data: UserAuth):
    """Позволяет пользователю аутентифицироваться."""
    user = await authenticate_user(
        email=user_data.email, password=user_data.password
    )

    if not user:
        raise IncorrectUserDataException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('my_booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('my_booking_access_token')
    return 'Пользователь вышел из системы.'


@router.get('/me', response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
