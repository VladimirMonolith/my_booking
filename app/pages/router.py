from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location

router = APIRouter(
    prefix='/pages',
    tags=['pages']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/hotels')
async def get_hotels_pages(
    request: Request,
    hotels=Depends(get_hotels_by_location)
):
    """Отображает html-шаблон страницы с отелями с выборкой по локации."""
    return templates.TemplateResponse(
        name='hotels.html', context={'request': request, 'hotels': hotels}
    )
