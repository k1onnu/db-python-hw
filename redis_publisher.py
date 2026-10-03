import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

if __name__ == "__main__":
    for i in range(5):
        msg = f"Сообщение №{i+1}"
        r.publish("news", msg)
        print(f"[PUBLISHED] {msg}")
        time.sleep(1)


"""
[PUBLISHED] Сообщение №1
[PUBLISHED] Сообщение №2
[PUBLISHED] Сообщение №3
[PUBLISHED] Сообщение №4
"""