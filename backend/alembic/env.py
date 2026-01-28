from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sys
import os
from alembic import context

# Add the parent directory (backend/) to sys.path so 'app' is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# this is the Alembic Config object
config = context.config

# Set up logging from alembic.ini (safe guard against missing file)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── IMPORTANT: Import your models' Base ────────────────────────────────
# Make sure all models are imported so they register with metadata
from app.models import Base           # adjust path if needed (e.g. app.database.base)

target_metadata = Base.metadata

# Optional: print a debug message during development
# print("Using metadata from:", target_metadata.tables.keys())  # uncomment to verify


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()