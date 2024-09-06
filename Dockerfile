FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-dev

COPY . .

EXPOSE 5000

CMD ["poetry", "run", "python", "app.py"]