import psycopg2
import os

# Verbindung herstellen
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5433"),
    database=os.getenv("POSTGRES_DB", "supplychain"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "password"),
)

# Cursor erstellen
cur = conn.cursor()

# Test-Query ausführen
cur.execute("SELECT version();")
version = cur.fetchone()
print(f"PostgreSQL Version: {version[0]}")

# Verbindung schließen
cur.close()
conn.close()

print("PostgreSQL funktioniert!")