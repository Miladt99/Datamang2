import psycopg2
import os

# Verbindung herstellen
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    database=os.getenv("POSTGRES_DB", "supplychain"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "password"),
)


cur = conn.cursor()

# Alle Tabellen auflisten
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cur.fetchall()
print("Erstellte Tabellen:")
for table in tables:
    print(f"- {table[0]}")

cur.close()
conn.close()

print(f"\nInsgesamt {len(tables)} Tabellen erstellt!")