# import uvicorn

from dataclasses import dataclass
from typing import Optional

from fastapi import Depends, FastAPI, Query

# from pydantic import BaseModel, Field

app = FastAPI(title='project')


@dataclass
class Test:
    id: int
    quality: Optional[str] = None
    period: Optional[int] = Query(None, ge=1, le=5)


@app.get('/')
async def test(
    test: Test = Depends()
):
    return 'Cjctn'


# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
