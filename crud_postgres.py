from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError

#Settings
DB_USER = "postgres"
DB_PASSWORD = "1369"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Test_base_python"

#Engine & metadata
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
metadata = MetaData()


#users
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("age", Integer, nullable=False),
)

metadata.create_all(engine)




def create_user(name, email, age):
    try:
        with engine.begin() as conn:
            stmt = insert(users).values(name=name, email=email, age=age).returning(users.c.id)
            result = conn.execute(stmt)
            new_id = result.scalar()
            print(f"User created with id={new_id}")
            return new_id
    except SQLAlchemyError as e:
        print("Error creating user: {e}")
        return None



  
def read_all_users():
    try:
        with engine.connect() as conn:
            result = conn.execute(select(users))
            rows = result.fetchall()
            print(f"Users found: {len(rows)}")
            for row in rows:
                print(row)
            return rows
    except SQLAlchemyError as e:
        print(f"Error while reading: {e}")
        return []




def read_user_by_id(user_id):
    try:
        with engine.connect() as conn:
            result = conn.execute(select(users).where(users.c.id == user_id))
            row = result.fetchone()
            if row: 
                print(row)
            else:
                print(f"User with id= {user_id} not found")
            return row
    except SQLAlchemyError as e:
        print(f"Error while reading: {e}")
        return None




def update_user(user_id, name=None, email=None, age=None):
    try:
        with engine.begin() as conn:
            values = {}
            if name is not None:
                values["name"] = name
            if email is not None:
                values["email"] = email
            if age is not None:
                values["age"] = age

            if not values:
                print("Nothing to update")
                return

            stmt = update(users).where(users.c.id == user_id).values(**values)
            result = conn.execute(stmt)
            if result.rowcount:
                print(f"User id={user_id} updated")
            else:
                print(f"User with id={user_id} not found")
    except SQLAlchemyError as e:
        print(f"Error during update: {e}")




def delete_user(user_id):
    try:
        with engine.begin() as conn:
            stmt = delete(users).where(users.c.id == user_id)
            result = conn.execute(stmt)
            if result.rowcount:
                print(f"User id={user_id} deleted")
            else:
                print(f"User with id={user_id} not found")
    except SQLAlchemyError as e:
        print(f"Error while deleting: {e}")



if __name__ == "__main__":
    print("\n--- Create user ---")
    uid1 = create_user("Иван Иванов", "ivan@mail.ru", 30)
    uid2 = create_user("Мария Петрова", "maria@mail.ru", 25)

    print("\n--- Read all users ---")
    read_all_users()

    print("\n--- Reading one ---")
    read_user_by_id(uid1)

    print("\n--- Update ---")
    update_user(uid1, age=31)

    print("\n--- Reading after update ---")
    read_user_by_id(uid1)

    print("\n--- Delete ---")
    delete_user(uid2)

    print("\n--- Final list ---")
    read_all_users()

    """
--- Create user ---
User created with id=1
User created with id=2

--- Read all users ---
Users found: 2
(1, 'Иван Иванов', 'ivan@mail.ru', 30)
(2, 'Мария Петрова', 'maria@mail.ru', 25)

--- Reading one ---
(1, 'Иван Иванов', 'ivan@mail.ru', 30)

--- Update ---
User id=1 updated

--- Reading after update ---
(1, 'Иван Иванов', 'ivan@mail.ru', 31)

--- Delete ---
User id=2 deleted

--- Final list ---
Users found: 1
(1, 'Иван Иванов', 'ivan@mail.ru', 31)"""