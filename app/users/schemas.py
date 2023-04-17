from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    """Модель регистрации пользователя."""

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Модель отображения пользователя."""

    id: int
    email: EmailStr

    class Config:
        orm_mode = True
