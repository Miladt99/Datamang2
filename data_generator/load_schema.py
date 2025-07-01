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

# SQL-Schema aus Datei lesen
with open('../sql/schema.sql', 'r', encoding='utf-8') as file:
    sql_commands = file.read()

# Schema ausführen
cur.execute(sql_commands)

# Änderungen speichern
conn.commit()

print("Schema erfolgreich geladen!")

# Tabellen auflisten
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cur.fetchall()
print(f"\nErstellte Tabellen ({len(tables)}):")
for table in tables:
    print(f"- {table[0]}")

cur.close()
conn.close()