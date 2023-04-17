from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response

from app.users.auth import get_password_hash, verify_password

from .auth import authenticate_user, create_access_token
from .dao import UserDAO
from .schemas import UserAuth

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/register')
async def register_user(user_data: UserAuth):
    """Регистрирует пользователя."""
    user = await UserDAO.get_object(email=user_data.email)

    if user:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Вы уже были зарегистрированы'
        )
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add_objects(
        email=user_data.email, hashed_password=hashed_password
    )
    return 'Вы успешно зарегистрировались'


@router.post('/login')
async def login_user(response: Response, user_data: UserAuth):
    """Позволяет пользователю аутентифицироваться."""
    user = await authenticate_user(email=user_data.email, password=user_data.password) 

    # user = await authenticate_user(**user_data)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Проверьте введенные данные или зарегистрируйтесь'
        )
    
    access_token = create_access_token({'sub': user.id})
    response.set_cookie('my_booking_access_token', access_token)
    return access_token

