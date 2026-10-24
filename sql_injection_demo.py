import psycopg2

DB = {
    "host": "localhost", "port": 5433,
    "dbname": "Test_base_python",
    "user": "postgres", "password": "1369"
}


def vulnerable(email):
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    query = f"SELECT id, name, email FROM orm_users WHERE email = '{email}'"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def safe(email):
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM orm_users WHERE email = %s", (email,))
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    payload = "' OR '1'='1"
    print("Vulnerable:", vulnerable(payload))
    print("Safe:", safe(payload))