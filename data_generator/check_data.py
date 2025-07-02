import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5433"),
        database=os.getenv("POSTGRES_DB", "supplychain"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
    )


def check_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Partnerunternehmen zählen
    cur.execute("SELECT COUNT(*) FROM partnerunternehmen")
    partner_count = cur.fetchone()[0]
    print(f"Partnerunternehmen: {partner_count}")
    
    # Transportdienstleister zählen
    cur.execute("SELECT COUNT(*) FROM transportdienstleister")
    transport_count = cur.fetchone()[0]
    print(f"Transportdienstleister: {transport_count}")
    
    # Produkte zählen
    cur.execute("SELECT COUNT(*) FROM produkt")
    produkt_count = cur.fetchone()[0]
    print(f"Produkte: {produkt_count}")
    
    # Beispieldaten anzeigen
    print("\nBeispiel-Partnerunternehmen:")
    cur.execute("SELECT * FROM partnerunternehmen LIMIT 3")
    for row in cur.fetchall():
        print(f"  {row}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_data()