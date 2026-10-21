# FastAPI Template

FastAPI asosidagi backend shabloni. Loyihada PostgreSQL, SQLAlchemy, Alembic
migratsiyalari, Redis, Celery hamda JWT orqali autentifikatsiya bor.

## Talablar

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (local ishga tushirish uchun)
- Docker va Docker Compose (konteynerda ishga tushirish uchun)

## Sozlash

Avval muhit sozlamalarini nusxalang:

```bash
cp .env.example .env
```

`SECRET_KEY` qiymatini albatta o'zgartiring.

`DATABASE_URL` ishlatish usuliga qarab quyidagicha bo'lishi kerak:

| Ishga tushirish usuli | `DATABASE_URL` |
| --- | --- |
| Local Python | `postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi` |
| Docker Compose | `postgresql+asyncpg://fastapi:fastapi@db:5432/fastapi` |

> Docker ichida `localhost` API konteynerining o'zini anglatadi. Shu sababli
> PostgreSQL uchun Docker servis nomi — `db` — ishlatiladi.

## Docker orqali ishga tushirish

`.env` ichidagi `DATABASE_URL`da host sifatida `db` ko'rsatilganini tekshiring,
so'ng barcha servislarni ishga tushiring:

```bash
docker compose up --build -d
```

Bu buyruq quyidagi servislarni ishga tushiradi: `api`, `db` (PostgreSQL),
`redis`, `celery-worker` va `celery-beat`.

Holat va loglarni tekshirish:

```bash
docker compose ps
docker compose logs -f api
```

API odatda `http://127.0.0.1:8000` manzilida bo'ladi. Quyidagi sahifalar
foydali:

- Health check: `GET /health`
- Swagger UI: `http://127.0.0.1:8000/docs`
- API prefiksi: `/api/v1`

To'xtatish:

```bash
docker compose down
```

Ma'lumotlar bazasi saqlanadi. Uni ham o'chirish kerak bo'lsa:

```bash
docker compose down -v
```

## Local ishga tushirish

Avval PostgreSQL va Redis ishga tushgan bo'lishi kerak. `.env`da PostgreSQL
hosti `localhost`, Redis URL'lari esa local Redis manziliga mos bo'lishi kerak.

Bog'liqliklarni o'rnating:

```bash
uv sync
```

API'ni development rejimida ishga tushiring:

```bash
uv run uvicorn app.main:app --reload
```

Yoki Invoke yordamida:

```bash
uv run inv run
```

Celery worker va scheduler kerak bo'lsa, alohida terminallarda ishga tushiring:

```bash
uv run inv worker
uv run inv beat
```

## Ma'lumotlar bazasi migratsiyalari

Alembic migratsiya fayllari `app/models/migrations/versions/` ichida saqlanadi.

### Birinchi yoki yangi migratsiyani yaratish

Model o'zgargandan keyin migration yarating:

```bash
uv run alembic revision --autogenerate -m "create users table"
```

Yaratilgan faylni ko'rib chiqing, so'ng uni bazaga qo'llang:

```bash
uv run alembic upgrade head
```

Docker ishlatayotganda shu buyruqlarni API konteyneri ichida bajaring:

```bash
docker compose exec api alembic revision --autogenerate -m "create users table"
docker compose exec api alembic upgrade head
```

> `docker compose up` migratsiyalarni avtomatik qo'llamaydi; ularni yuqoridagi
> `alembic upgrade head` buyrug'i bilan alohida qo'llang.

### Foydali Alembic buyruqlari

```bash
# Hozirgi migration versiyasi
uv run alembic current

# Mavjud migrationlar tarixi
uv run alembic history

# Bitta oldingi versiyaga qaytish
uv run alembic downgrade -1
```

Docker ichida ishlaganda `uv run alembic` o'rniga `docker compose exec api alembic`
dan foydalaning.

## Admin foydalanuvchi yaratish

Migratsiyalar qo'llangandan so'ng test admin yarating:

```bash
uv run inv create-admin
```

Buyruq `admin` username va `admin` paroli bilan foydalanuvchi yaratadi. Ishlab
chiqarish muhitida bu ma'lumotlarni ishlatmang; kerak bo'lsa foydalanuvchini
to'g'ridan-to'g'ri yarating:

```bash
uv run python scripts/create_user.py admin \
  --username admin \
  --full-name "Admin User" \
  --password "kuchli-parol"
```

## API autentifikatsiyasi

Login endpointi:

```text
POST /api/v1/auth/login/
```

Muvaffaqiyatli login JWT `access_token` qaytaradi. Himoyalangan endpointlarga
so'rov yuborishda tokenni quyidagicha jo'nating:

```text
Authorization: Bearer <access_token>
```

Masalan, joriy foydalanuvchi profili:

```text
GET /api/v1/auth/profile/
```
