FROM python:3.12

RUN pip3 install --upgrade pip && pip3 install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

CMD ["gunicorn", "--bind", "0:8000", "config.wsgi"]