from fastapi import Response, UploadFile, APIRouter,status
import shutil

router = APIRouter(
    prefix='/images',
    tags=['images']
)


@router.post('/hotels', status_code=status.HTTP_201_CREATED)
async def download_hotels_images(file: UploadFile, file_id: int, ):
    """."""
    with open(f'app/static/images/{file_id}.webp', 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    return 'Файл успешно загружен.'
