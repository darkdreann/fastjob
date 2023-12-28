FROM python:3.11.7

RUN mkdir -p /app/api

WORKDIR /app

COPY requirements.txt ./
COPY api ./api/
COPY manage.py ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python manage.py runserver