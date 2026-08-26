import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[2] / "tripmate.db"
DATABASE_URL = os.getenv(
    "TRIPMATE_DATABASE_URL",
    f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


Base = declarative_base()


def init_db():
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
