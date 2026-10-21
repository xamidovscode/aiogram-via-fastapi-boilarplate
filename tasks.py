import subprocess
from invoke import task

DOCKER_CONTAINER = "app-api"


def _is_docker_running():
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", DOCKER_CONTAINER],
            capture_output=True, text=True
        )
        return result.stdout.strip() == "true"
    except FileNotFoundError:
        return False


@task
def build(c):
    c.run("docker compose up --build -d")


@task
def down(c):
    c.run("docker compose down")


@task
def migrate(c):
    c.run(f"docker exec {DOCKER_CONTAINER} alembic upgrade head")


@task
def run(c):
    c.run("uvicorn app.main:app --reload")


@task
def create_admin(c):
    """admin/admin username va parol bilan admin yaratish."""
    cmd = 'python scripts/create_user.py admin --username admin --full-name "Admin User" --password admin'
    if _is_docker_running():
        c.run(f"docker exec {DOCKER_CONTAINER} {cmd}")
    else:
        c.run(cmd)


@task
def worker(c):
    """Celery worker'ni local'da ishga tushirish."""
    c.run("celery -A app.core.celery.celery_app worker --loglevel=info --concurrency=4")


@task
def beat(c):
    """Celery beat'ni local'da ishga tushirish."""
    c.run("celery -A app.core.celery.celery_app beat --loglevel=info --schedule /tmp/celerybeat-schedule")


@task
def flower(c):
    """Celery flower monitoring UI (http://localhost:5555)."""
    c.run("celery -A app.core.celery.celery_app flower --port=5555")