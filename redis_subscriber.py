import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

if __name__ == "__main__":
    pubsub = r.pubsub()
    pubsub.subscribe("news")
    print("[SUBSCRIBED] Ждём сообщения в канале 'news'...")

    for message in pubsub.listen():
        if message["type"] == "message":
            print(f"[RECEIVED] {message['data']}")

"""
[SUBSCRIBED] Ждём сообщения в канале 'news'...
[RECEIVED] Сообщение №1
[RECEIVED] Сообщение №2
[RECEIVED] Сообщение №3
[RECEIVED] Сообщение №4
[RECEIVED] Сообщение №5
"""