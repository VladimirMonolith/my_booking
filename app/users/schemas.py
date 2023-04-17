from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    """Модель регистрации и аутентификации пользователя."""

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Модель отображения пользователя."""

    id: int
    email: EmailStr

    class Config:
        orm_mode = True
