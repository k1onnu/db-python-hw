import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_user_from_db(user_id):
    """Имитация долгого запроса в БД."""
    time.sleep(1)
    return {"id": user_id, "name": f"User{user_id}", "email": f"user{user_id}@mail.ru"}


def get_user(user_id, ttl=10):
    """Получить пользователя с кешированием."""
    key = f"user:{user_id}"

    cached = r.get(key)
    if cached:
        print(f"[CACHE HIT] {key}")
        return json.loads(cached)

    print(f"[CACHE MISS] {key} — идём в БД")
    user = get_user_from_db(user_id)
    r.setex(key, ttl, json.dumps(user))
    return user


if __name__ == "__main__":
    print("Первый запрос (долго):")
    print(get_user(1))

    print("\nВторой запрос (мгновенно из кеша):")
    print(get_user(1))

    print("\nTTL ключа user:1 =", r.ttl("user:1"), "сек")

    print("\nЖдём 11 секунд, кеш истечёт...")
    time.sleep(11)

    print("\nТретий запрос (снова из БД):")
    print(get_user(1))