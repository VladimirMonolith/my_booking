FROM python:3.9

RUN mkdir /my_booking

WORKDIR /my_booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# предоставляет доступ для запуска скрипта, если это необходимо
# RUN chmod a+x /my_booking/docker/*.sh 

# RUN alembic upgrade head

# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]