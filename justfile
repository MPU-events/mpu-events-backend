set dotenv-load := true

pythonpath := "src"
env := env_var_or_default("ENV_FOR_DYNACONF", "local")

default:
    @just --list

run:
    PYTHONPATH={{pythonpath}} ENV_FOR_DYNACONF={{env}} uv run uvicorn mpu_events.main:app --reload --host 0.0.0.0 --port 8001

migrate:
    PYTHONPATH={{pythonpath}} ENV_FOR_DYNACONF={{env}} uv run alembic upgrade head

makemigration name:
    PYTHONPATH={{pythonpath}} ENV_FOR_DYNACONF={{env}} uv run alembic revision --autogenerate -m "{{name}}"

downgrade:
    PYTHONPATH={{pythonpath}} ENV_FOR_DYNACONF={{env}} uv run alembic downgrade -1

history:
    PYTHONPATH={{pythonpath}} uv run alembic history

current:
    PYTHONPATH={{pythonpath}} uv run alembic current

build:
    docker compose build

up:
    docker compose up -d

down:
    docker compose down

restart:
    docker compose restart app

logs:
    docker compose logs -f app

docker-migrate:
    docker compose exec app uv run alembic upgrade head