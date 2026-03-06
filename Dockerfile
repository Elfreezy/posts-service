FROM python:3.12-alpine

# Устанавливаем системные зависимости для psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 

WORKDIR /user_service

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]