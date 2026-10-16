import os
import pymongo
from faker import Faker
import random


class Products:
    def __init__(self):
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.coll = pymongo.MongoClient(uri)["shop_db"]["products"]

    def indexes(self):
        self.coll.create_index([("category", 1), ("price", -1)])
        self.coll.create_index([("seller.id", 1)])
        self.coll.create_index([("tags", 1)])
        self.coll.create_index([("attributes.color", 1)])
        print("Indexes:", list(self.coll.index_information().keys()))

    def fill(self, n=100):
        fake = Faker('ru_RU')
        self.coll.delete_many({})
        sellers = [{"id": i, "name": f"Seller{i}", "city": fake.city()} for i in range(1, 6)]
        docs = []
        for i in range(n):
            docs.append({
                "sku": f"SKU-{i}",
                "name": fake.catch_phrase(),
                "category": random.choice(["electronics", "clothing", "books"]),
                "price": round(random.uniform(100, 50000), 2),
                "tags": random.sample(["sale", "new", "premium"], k=2),
                "attributes": {
                    "color": random.choice(["black", "white", "red"]),
                    "dimensions": {"l": random.randint(1, 100), "w": random.randint(1, 100)}
                },
                "seller": random.choice(sellers),
                "reviews": [{"user": fake.name(), "rating": random.randint(1, 5)} for _ in range(random.randint(0, 4))]
            })
        self.coll.insert_many(docs)
        print(f"Inserted: {n}")

    # CRUD-like методы
    def by_category(self, cat):
        return list(self.coll.find({"category": cat}))

    def by_seller(self, sid):
        return list(self.coll.find({"seller.id": sid}))

    def by_tag(self, tag):
        return list(self.coll.find({"tags": tag}))

    def by_color(self, color):
        return list(self.coll.find({"attributes.color": color}))

    def update_price(self, sku, price):
        return self.coll.update_one({"sku": sku}, {"$set": {"price": price}}).modified_count

    def delete(self, sku):
        return self.coll.delete_one({"sku": sku}).deleted_count

    # Агрегации
    def top_rated(self, n=5):
        return list(self.coll.aggregate([
            {"$match": {"reviews.0": {"$exists": True}}},
            {"$addFields": {"avg": {"$avg": "$reviews.rating"}, "cnt": {"$size": "$reviews"}}},
            {"$sort": {"avg": -1, "cnt": -1}},
            {"$limit": n},
            {"$project": {"_id": 0, "name": 1, "avg": 1, "cnt": 1}}
        ]))

    def avg_by_category(self):
        return list(self.coll.aggregate([
            {"$group": {"_id": "$category", "avg_price": {"$avg": "$price"}, "count": {"$sum": 1}}},
            {"$sort": {"avg_price": -1}}
        ]))

    def top_sellers(self, n=3):
        return list(self.coll.aggregate([
            {"$group": {"_id": "$seller.id", "name": {"$first": "$seller.name"},
                        "avg_price": {"$avg": "$price"}, "total": {"$sum": 1}}},
            {"$sort": {"avg_price": -1}},
            {"$limit": n}
        ]))


if __name__ == "__main__":
    p = Products()
    p.fill(100)
    p.indexes()

    print("\nby category:", len(p.by_category("electronics")))
    print("by seller:", len(p.by_seller(1)))
    print("by tag:", len(p.by_tag("sale")))
    print("by color:", len(p.by_color("red")))

    print("update price:", p.update_price("SKU-0", 9999))
    print("delete:", p.delete("SKU-99"))

    print("\nTop rated:")
    for r in p.top_rated(): print(r)

    print("\nAvg by category:")
    for r in p.avg_by_category(): print(r)

    print("\nTop sellers:")
    for r in p.top_sellers(): print(r)

    # Проверка использования индекса
    plan = p.coll.find({"category": "electronics", "price": {"$gte": 1000}}).explain()
    print("\nIndex used:", plan["queryPlanner"]["winningPlan"].get("stage"))