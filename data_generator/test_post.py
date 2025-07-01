import psycopg2

# Verbindung herstellen
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="supplychain",
    user="postgres",
    password="password"
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