import json
from datetime import datetime
from typing import Iterable

from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelDAO
from app.logger import logger
from app.rooms.dao import RoomDAO
from app.users.dao import UserDAO

TABLE_MODEL_MAP = {
    'hotels': HotelDAO,
    'rooms': RoomDAO,
    'bookings': BookingDAO,
    'users': UserDAO
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    """Конвертирует csv в формат PosgreSQL."""
    try:
        data = []
        for row in csv_iterable:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif key == 'services':
                    row[key] = json.loads(value.replace("'", '"'))
                elif 'date' in key:
                    row[key] = datetime.strptime(value, '%Y-%m-%d')
            data.append(row)
        return data
    except Exception:
        logger.error(
            'Не удается конвертировать CSV в формат БД', exc_info=True
        )
