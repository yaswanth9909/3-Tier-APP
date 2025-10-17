import os, json, psycopg2, psycopg2.extras

DSN = os.getenv(
    "POSTGRES_DSN",
    "postgresql://postgres:postgres@db.three-tier.svc.cluster.local:5432/postgres"
)

def main():
    with psycopg2.connect(DSN) as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT COUNT(*) AS c FROM orders")
        count = cur.fetchone()["c"]
        cur.execute("INSERT INTO order_stats(total_orders) VALUES (%s)", (count,))
        conn.commit()
    print("Recorded total_orders:", count)

if __name__ == "__main__":
    main()

