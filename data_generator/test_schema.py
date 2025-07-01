import psycopg2

# Verbindung herstellen
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="supplychain",
    user="postgres",
    password="password"
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