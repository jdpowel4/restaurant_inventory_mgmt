import pytest
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from decimal import Decimal

from inventory_app.common.base import Base
import inventory_app.models
from tests.factories import make_unit


@pytest.fixture(scope="session")
def engine():

    engine = create_engine(
        "sqlite:///:memory:",
        future=True
    )
    print(Base.metadata.tables.keys())
    
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine) ->Generator[Session, None, None]:

    SessionLocal = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=True,
        future=True
    )

    session = SessionLocal()

    yield session

    session.rollback()
    session.close()


