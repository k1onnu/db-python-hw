import uuid
import pytest
from faker import Faker
from sqlalchemy.orm import Session
from models import engine, Base, User, Post


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(engine)
    yield engine


@pytest.fixture
def session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def faker_ru():
    return Faker('ru_RU')


@pytest.fixture
def make_user(session, faker_ru):
    def _make(**kwargs):
        data = {
            "name": faker_ru.name(),
            "email": f"{uuid.uuid4().hex[:8]}@example.com",
            "age": faker_ru.random_int(18, 80),
            "bio": faker_ru.sentence(),
        }
        data.update(kwargs)
        user = User(**data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return _make


@pytest.fixture
def make_post(session, faker_ru):
    def _make(user_id, **kwargs):
        data = {
            "title": faker_ru.sentence(nb_words=4),
            "content": faker_ru.paragraph(),
            "user_id": user_id,
        }
        data.update(kwargs)
        post = Post(**data)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    return _make