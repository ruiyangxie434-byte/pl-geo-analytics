from pathlib import Path

from alembic import command
from alembic.config import Config

from app.core.config import get_settings
from app.database.seed import seed_sample_data
from app.database.session import SessionLocal


def upgrade_database() -> None:
    settings = get_settings()
    backend_root = Path(__file__).resolve().parents[2]
    alembic_config = Config(str(backend_root / "alembic.ini"))
    alembic_config.set_main_option(
        "script_location",
        str(backend_root / "migrations"),
    )
    alembic_config.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(alembic_config, "head")


def initialize_database() -> None:
    settings = get_settings()

    if settings.auto_create_database:
        upgrade_database()

    if settings.seed_sample_data:
        with SessionLocal() as session:
            seed_sample_data(session)


if __name__ == "__main__":
    initialize_database()
    print("Database ready: schema applied and sample data checked.")
