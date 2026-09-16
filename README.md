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
