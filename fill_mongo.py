import pymongo
from faker import Faker
import random
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test_database"]
collection = db["users"]
collection.delete_many({})

fake = Faker('ru_RU')
data = []
for i in range(100):
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
    birth_datetime = datetime.combine(birth_date, datetime.min.time())
    record = {
        "user_id": i + 1,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "age": random.randint(18, 80),
        "balance": round(random.uniform(0, 10000), 2),
        "is_active": random.choice([True, False]),
        "registered_at": fake.date_time_between(start_date='-2y', end_date='now'),
        "birth_date": birth_datetime,
        "address": {
            "city": fake.city(),
            "street": fake.street_name(),
            "building": fake.building_number()
        },
        "hobbies": random.sample(['reading', 'swimming', 'gaming', 'traveling', 'cooking', 'music'], k=random.randint(1,3))
    }
    data.append(record)

result = collection.insert_many(data)
print(f"Added: {len(result.inserted_ids)}")
print(f"Total: {collection.count_documents({})}")
print("Sample:", collection.find_one())
client.close()