## Задание 1. Знакомство с MongoDB
Скрипт `fill_mongo.py` подключается к локальной MongoDB, создаёт коллекцию `users`
в базе `test_database` и наполняет её 100 сгенерированными записями
(имя, email, возраст, баланс, дата регистрации, адрес, хобби).

## Задание 2. CRUD для PostgreSQL через SQLAlchemy Core
Скрипт `crud_postgres.py` демонстрирует базовые CRUD-операции
над таблицей `users` (id, name, email, age):
- create_user — создание
- read_all_users / read_user_by_id — чтение
- update_user — обновление
- delete_user — удаление

## Задание 3. ORM, Alembic и каскадное удаление
### Модели
Файл `models.py` содержит две связанные ORM-модели (связь OneToMany):
- `User` (таблица `orm_users`) — id, name, email, age, bio
- `Post` (таблица `orm_posts`) — id, title, content, user_id

Связь реализована через `relationship(back_populates=...)` с каскадным удалением:
`cascade="all, delete-orphan"` + `ondelete="CASCADE"` на уровне БД.

### Миграции Alembic
- `e5a9a163a89b_create_orm_users_and_orm_posts.py` — создание таблиц `orm_users` и `orm_posts`
- `52806ef93ca3_add_bio_to_orm_users.py` — рефакторинг: добавление поля `bio` в `orm_users`

Применяются командой:
```bash
alembic upgrade head