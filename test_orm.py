import pytest
from sqlalchemy.exc import IntegrityError
from models import User, Post

def test_create_user(session, faker_ru):
    user = User(
        name=faker_ru.name(),
        email=faker_ru.email(),
        age=faker_ru.random_int(18, 80),
        bio=faker_ru.sentence(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.name is not None
    assert "@" in user.email


def test_read_user(session, make_user):
    created = make_user()
    found = session.get(User, created.id)

    assert found is not None
    assert found.email == created.email
    assert found.name == created.name


def test_update_user(session, make_user):
    user = make_user(age=25)
    user.age = 30
    user.bio = "обновлено"
    session.commit()
    session.refresh(user)

    assert user.age == 30
    assert user.bio == "обновлено"


def test_delete_user(session, make_user):
    user = make_user()
    user_id = user.id

    session.delete(user)
    session.commit()

    assert session.get(User, user_id) is None


def test_create_post_for_user(session, make_user, make_post):
    user = make_user()
    post = make_post(user.id, title="Мой пост")

    assert post.id is not None
    assert post.user_id == user.id
    assert post.title == "Мой пост"


def test_user_posts_relationship(session, make_user, make_post):
    user = make_user()
    make_post(user.id, title="Пост 1")
    make_post(user.id, title="Пост 2")

    session.refresh(user)
    assert len(user.posts) == 2
    assert {p.title for p in user.posts} == {"Пост 1", "Пост 2"}


def test_cascade_delete(session, make_user, make_post):
    user = make_user()
    make_post(user.id, title="Пост для каскада")
    post_id = user.posts[0].id

    session.delete(user)
    session.commit()

    assert session.get(User, user.id) is None
    assert session.get(Post, post_id) is None

def test_create_user_duplicate_email(session, make_user, faker_ru):
    existing = make_user()

    duplicate = User(
        name=faker_ru.name(),
        email=existing.email,
        age=20,
    )
    session.add(duplicate)

    with pytest.raises(IntegrityError):
        session.commit()


def test_create_user_without_name(session, faker_ru):
    user = User(name=None, email=faker_ru.email(), age=25)
    session.add(user)

    with pytest.raises(IntegrityError):
        session.commit()


def test_create_user_without_email(session, faker_ru):
    user = User(name=faker_ru.name(), email=None, age=25)
    session.add(user)

    with pytest.raises(IntegrityError):
        session.commit()


def test_read_nonexistent_user(session):
    user = session.get(User, 999_999)
    assert user is None


def test_update_nonexistent_user(session):
    user = session.get(User, 999_999)
    assert user is None


def test_delete_nonexistent_user(session):
    user = session.get(User, 999_999)
    if user is not None:
        session.delete(user)
        session.commit()
    assert session.get(User, 999_999) is None


def test_create_post_with_invalid_user_id(session, faker_ru):
    post = Post(
        title=faker_ru.sentence(nb_words=3),
        content=faker_ru.paragraph(),
        user_id=999_999,
    )
    session.add(post)

    with pytest.raises(IntegrityError):
        session.commit()