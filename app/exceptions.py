from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже существует.'
)

IncorrectUserDataException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Проверьте введённые данные.'
)

NotAuthUserException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Вы не аутентифицированы. Выполните вход в систему.'
)

TokenInvalidException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен доступа некорректен.'
)

TokenExpireException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Время сессии истекло. Выполните вход в систему.'
)

TokenInvalidDataException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Сессия некорректна. Переданные данные некорректны.'
)
