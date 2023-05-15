from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    """Класс для отображения пользователей в админке."""

    column_list = [User.id, User.email, User.booking]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class HotelAdmin(ModelView, model=Hotel):
    """Класс для отображения отелей в админке."""

    column_list = [c.name for c in Hotel.__table__.c]
    column_list += [Hotel.rooms]
    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'


class RoomAdmin(ModelView, model=Room):
    """Класс для отображения комнат отелей в админке."""

    column_list = [c.name for c in Room.__table__.c]
    column_list += [Room.hotel, Room.booking]
    name = 'Номер'
    name_plural = 'Номера'
    icon = 'fa-solid fa-bed'


class BookingAdmin(ModelView, model=Booking):
    """Класс для отображения бронирований в админке."""

    column_list = [c.name for c in Booking.__table__.c]
    column_list += [Booking.user]
    name = 'Бронирование'
    name_plural = 'Бронирования'
    icon = 'fa-solid fa-book'
