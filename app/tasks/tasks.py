from pathlib import Path

from PIL import Image

from app.tasks.celery import celery


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