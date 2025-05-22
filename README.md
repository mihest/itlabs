# Тестовое задание ITLABS

### Запуск проекта через Docker
Для запуска переименуйте .env.example в .env (настраивать не надо, environment прописаны в docker-compose.yaml)<br>
В корне проекта прописать
```shell
    docker compose up --build -d
```
Команда соберёт 2 контейнера:
1. База данных (PostgreSQL) 
2. App (миграции alembic + backend fastapi)

### Запуск проекта через cmd
Для запуска переименуйте .env.example в .env и переменные для подключения к БД PostgreSQL<br>
В корне проекта прописать
```shell
    pip install uv
    uv sync --no-dev
    alembic upgrade head
    python -m src.main
```

### Запуск тестов
Для запуска переименуйте .env.example в .env и переменные для подключения к тестовой БД PostgreSQL<br>
В корне проекта прописать
```shell
    pip install uv
    uv sync
    pytest
```

### Используемый стек технологий
* Python 3.12 - язык программирования на котором разрабатывался проект
* PostgreSQL - используемая БД в проекте
* SQLAlchemy 2.0.41 - ORM система для работы с БД
* AsyncPg 0.30.0 - асинхронный коннектор для связи с БД
* Alembic 1.15.2 - миграции БД
* SQLAdmin 0.20.1 - админ панель
* FastAPI 0.115.12 - фреймворк на котором разрабатывался проект
* Pytest 8.3.5 - для написания тестов
