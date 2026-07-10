from logging.config import fileConfig
from pathlib import Path
import os

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

from app.database.base import Base
import back_end.app.domains

# Carrega o .env da raiz do projeto
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

config = context.config

DATABASE_URL = (
            f"postgresql+psycopg://"
            f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
            f"/{os.getenv('DB_NAME')}"
        )

config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# IMPORTANTE
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrations sem conexão com banco."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrations conectado ao banco."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()