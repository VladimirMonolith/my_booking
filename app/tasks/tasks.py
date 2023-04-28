import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def photo_processing(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    big_image_resized = image.resize((1000, 500))
    small_image_resized = image.resize((300, 150))
    big_image_resized.save(f'app/static/images/big_resized_{image_path.name}')
    small_image_resized.save(
        f'app/static/images/small_resized_{image_path.name}'
    )


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_to_user = settings.SMTP_USER
    email_content = create_booking_confirmation_template(
        booking=booking, email_to=email_to_user
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email_content)
