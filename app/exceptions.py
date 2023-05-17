from fastapi import HTTPException, status


class MyBookingException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(MyBookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует.'


class IncorrectUserDataException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Проверьте введённые данные.'


class NotAuthUserException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Вы не аутентифицированы. Выполните вход в систему.'


class TokenInvalidException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен доступа некорректен.'


class TokenExpireException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Время сессии истекло. Выполните вход в систему.'


class TokenInvalidDataException(MyBookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Сессия некорректна. Переданные данные некорректны.'


class RoomCantBookedException(MyBookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Свободных комнат данного типа не осталось.'


class NotFoundException(MyBookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Данные не найдены.'


class CannotAddDataToDatabase(MyBookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ('Не удалось добавить запись в базу данных. '
              'Проверьте корректность данных.')


class CannotProcessCSV(MyBookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Не удалось обработать CSV файл.'
