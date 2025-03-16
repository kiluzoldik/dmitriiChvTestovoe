FROM python:3.10

RUN pip install --no-cache-dir poetry

WORKDIR /app

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD alembic upgrade head; python app/main.py