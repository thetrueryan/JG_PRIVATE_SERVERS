FROM python:3.12.3

WORKDIR /jg_servers_app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

WORKDIR /jg_servers_app/src

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "alembic upgrade head && python main.py"]