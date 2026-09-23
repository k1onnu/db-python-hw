from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import engine, User, Post


def create_user(name, email, age, bio=None):
    try:
        with Session(engine) as session:
            user = User(name=name, email=email, age=age, bio=bio)
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"Created: {user}")
            return user.id
    except SQLAlchemyError as e:
        print(f"Error creating user: {e}")
        return None


def create_post(user_id, title, content):
    try:
        with Session(engine) as session:
            post = Post(user_id=user_id, title=title, content=content)
            session.add(post)
            session.commit()
            session.refresh(post)
            print(f"Created: {post}")
            return post.id
    except SQLAlchemyError as e:
        print(f"Error creating post: {e}")
        return None


def read_all_users():
    try:
        with Session(engine) as session:
            users = session.query(User).all()
            print(f"Found {len(users)} users")
            for u in users:
                print(f"  {u} | posts={len(u.posts)}")
            return users
    except SQLAlchemyError as e:
        print(f"Error reading: {e}")
        return []


def read_user_with_posts(user_id):
    try:
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                print(f"User {user_id} not found")
                return None
            print(user)
            for p in user.posts:
                print(f"  └─ {p}")
            return user
    except SQLAlchemyError as e:
        print(f"Error reading: {e}")
        return None


def update_user(user_id, **fields):
    try:
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                print(f"User {user_id} not found")
                return
            for key, value in fields.items():
                setattr(user, key, value)
            session.commit()
            print(f"Updated: {user}")
    except SQLAlchemyError as e:
        print(f"Error updating: {e}")


def delete_user(user_id):
    try:
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                print(f"User {user_id} not found")
                return
            session.delete(user)
            session.commit()
            print(f"Deleted user {user_id} (posts removed by cascade)")
    except SQLAlchemyError as e:
        print(f"Error deleting: {e}")


if __name__ == "__main__":
    print("\nCreate users")
    uid1 = create_user("Иван Иванов", "ivan_orm@mail.ru", 30, "Люблю Python")
    uid2 = create_user("Мария Петрова", "maria_orm@mail.ru", 25, "Пишу стихи")

    print("\nCreate posts")
    create_post(uid1, "Первый пост", "Привет, мир!")
    create_post(uid1, "Второй пост", "SQLAlchemy прикольный!")
    create_post(uid2, "Третий пост", "Как хорошо!")

    print("\nRead all users")
    read_all_users()

    print("\nRead user with posts")
    read_user_with_posts(uid1)

    print("\nUpdate user")
    update_user(uid1, age=31, bio="Python & PostgreSQL")

    print("\nDelete user (cascade)")
    delete_user(uid1)

    print("\nFinal check")
    read_all_users()
    with Session(engine) as session:
        posts = session.query(Post).all()
        print(f"Posts left in DB: {len(posts)}")

        """
Create users
Created: User(id=1, name='Иван Иванов', age=30)
Created: User(id=2, name='Мария Петрова', age=25)

Create posts
Created: Post(id=1, title='Первый пост', user_id=1)
Created: Post(id=2, title='Второй пост', user_id=1)
Created: Post(id=3, title='Третий пост', user_id=2)

Read all users
Found 2 users
  User(id=1, name='Иван Иванов', age=30) | posts=2
  User(id=2, name='Мария Петрова', age=25) | posts=1

Read user with posts
User(id=1, name='Иван Иванов', age=30)
  └─ Post(id=1, title='Первый пост', user_id=1)
  └─ Post(id=2, title='Второй пост', user_id=1)

Update user
Updated: User(id=1, name='Иван Иванов', age=31)

Delete user (cascade)
Deleted user 1 (posts removed by cascade)

Final check
Found 1 users
  User(id=2, name='Мария Петрова', age=25) | posts=1
Posts left in DB: 1
        """