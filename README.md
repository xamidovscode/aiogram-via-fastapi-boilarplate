# Шаблон FastAPI

Шаблон backend-приложения на FastAPI. В проект включены PostgreSQL, SQLAlchemy,
миграции Alembic, Redis, Celery и JWT-аутентификация.

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) для локального запуска
- Docker и Docker Compose для запуска в контейнерах

## Настройка

Сначала скопируйте файл настроек среды:

```bash
cp .env.example .env
```

Обязательно измените значение `SECRET_KEY`.

Для запуска Telegram-бота укажите токен, полученный от BotFather:

```dotenv
BOT_TOKEN=your-telegram-bot-token
```

Выберите режим работы бота:

```dotenv
BOT_MODE=polling
```

Для webhook замените режим и укажите публичный HTTPS-адрес приложения:

```dotenv
BOT_MODE=webhook
WEBHOOK_BASE_URL=https://example.com
WEBHOOK_PATH=/telegram/webhook
WEBHOOK_SECRET=telegram-webhook-secret
```

В режиме webhook Telegram отправляет обновления на
`https://example.com/telegram/webhook`. В режиме polling этот путь возвращает
`404`, а бот получает обновления напрямую от Telegram.

Значение `DATABASE_URL` зависит от способа запуска:

| Способ запуска | `DATABASE_URL` |
| --- | --- |
| Локальный Python | `postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi` |
| Docker Compose | `postgresql+asyncpg://fastapi:fastapi@db:5432/fastapi` |

> В Docker `localhost` указывает на сам контейнер API. Поэтому для PostgreSQL
> используется имя Docker-сервиса `db`.

## Запуск через Docker

Убедитесь, что в `.env` хостом в `DATABASE_URL` указан `db`, затем запустите
все сервисы:

```bash
docker compose up --build -d
```

Будут запущены сервисы `api`, `db` (PostgreSQL), `redis`, `celery-worker` и
`celery-beat`.

Проверка статуса и логов:

```bash
docker compose ps
docker compose logs -f api
```

API по умолчанию доступен по адресу `http://127.0.0.1:8000`.

- Проверка состояния: `GET /health`
- Swagger UI: `http://127.0.0.1:8000/docs`

Остановка:

```bash
docker compose down
```

База данных будет сохранена. Чтобы удалить и её:

```bash
docker compose down -v
```

## Локальный запуск

Сначала запустите PostgreSQL и Redis. В `.env` хост PostgreSQL должен быть
`localhost`, а URL Redis — соответствовать локальному Redis.

Установите зависимости:

```bash
uv sync
```

Запустите API в режиме разработки:

```bash
uv run uvicorn app.main:app --reload
```

Или через Invoke:

```bash
uv run inv run
```

При необходимости запустите worker и планировщик Celery в отдельных терминалах:

```bash
uv run inv worker
uv run inv beat
```

## Структура Telegram-бота

```text
app/bot/
├── dispatcher.py
├── runner.py
└── handlers/
    └── start.py
```

Бот запускается вместе с FastAPI. Новые обработчики добавляйте в
`app/bot/handlers/`, затем подключайте их в `app/bot/handlers/__init__.py`.

## Миграции базы данных

Файлы миграций Alembic хранятся в `app/models/migrations/versions/`.

### Создание первой или новой миграции

После изменения модели создайте миграцию:

```bash
uv run alembic revision --autogenerate -m "create users table"
```

Проверьте созданный файл, затем примените миграцию:

```bash
uv run alembic upgrade head
```

При использовании Docker выполните эти команды внутри контейнера API:

```bash
docker compose exec api alembic revision --autogenerate -m "create users table"
docker compose exec api alembic upgrade head
```

> `docker compose up` не применяет миграции автоматически. Выполните
> `alembic upgrade head` отдельно.

### Полезные команды Alembic

```bash
# Текущая версия миграции
uv run alembic current

# История миграций
uv run alembic history

# Откат на одну версию
uv run alembic downgrade -1
```

В Docker используйте `docker compose exec api alembic` вместо `uv run alembic`.

## Создание администратора

После применения миграций создайте тестового администратора:

```bash
uv run inv create-admin
```

Команда создаст пользователя с именем `admin` и паролем `admin`. Не используйте
эти данные в production; при необходимости создайте пользователя вручную:

```bash
uv run python scripts/create_user.py admin \
  --username admin \
  --full-name "Admin User" \
  --password "kuchli-parol"
```
