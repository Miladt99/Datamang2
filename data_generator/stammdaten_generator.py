import psycopg2
import random
from datetime import datetime
import os

def log_metadata(conn, table_name, source):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO metadata (table_name, created_at, source) VALUES (%s, %s, %s)",
        (table_name, datetime.now(), source),
    )
    conn.commit()
    cur.close()

# Verbindung zur PostgreSQL-Datenbank
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5433"),
        database=os.getenv("POSTGRES_DB", "supplychain"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
    )


# Beispieldaten für Partnerunternehmen
partner_typen = ["Lieferant", "Kunde", "Logistikpartner", "Hersteller", "Händler"]
partner_namen = [
    "BananaCorp GmbH", "Tropical Fruits Ltd", "Green Harvest AG", "Fresh Supply Co",
    "Organic Farms Inc", "Premium Fruits GmbH", "Global Logistics Ltd", "Fast Track AG",
    "Quality Control GmbH", "Best Fruits Ltd", "Fresh Direct AG", "Tropical Express Co"
]

# Beispieldaten für Transportdienstleister
dienstleister_typen = ["Spedition", "Logistikunternehmen", "Transport AG", "Express Service"]
dienstleister_namen = [
    "SpeedLog GmbH", "FastTrack AG", "Express Logistics Ltd", "Quick Transport Co",
    "Reliable Shipping GmbH", "Global Express AG", "Premium Logistics Ltd", "Swift Delivery Co"
]

def generate_partnerunternehmen(conn, anzahl=10, fehlerquote=0.2):
    for i in range(anzahl):
        name = random.choice(partner_namen) + f" {i+1}"
        typ = random.choice(partner_typen)
        adresse = random.choice(adressen)
        ansprechpartner = f"Max Mustermann {i+1}"

        # Fehler einbauen
        if random.random() < fehlerquote:
            fehlerart = random.choice(["leer", "tippfehler", "ungueltig"])
            if fehlerart == "leer":
                # Mache einen Wert leer
                if random.random() < 0.5:
                    name = None
                else:
                    adresse = None
            elif fehlerart == "tippfehler":
                name = name.replace("a", "x")  # Simpler Tippfehler
            elif fehlerart == "ungueltig":
                typ = "???"

        cur.execute("""
            INSERT INTO partnerunternehmen (name, typ, adresse, ansprechpartner)
            VALUES (%s, %s, %s, %s)
        """, (name, typ, adresse, ansprechpartner))
    conn.commit()
    log_metadata(conn, "partnerunternehmen", "stammdaten_generator.generate_partnerunternehmen")
    cur.close()
    print(f"{anzahl} Partnerunternehmen (inkl. fehlerhafte) erstellt")

# Transportdienstleister generieren
def generate_transportdienstleister(conn, anzahl=5):
    cur = conn.cursor()
    
    for i in range(anzahl):
        name = random.choice(dienstleister_namen) + f" {i+1}"
        typ = random.choice(dienstleister_typen)
        adresse = random.choice(adressen)
        ansprechpartner = f"Anna Logistik {i+1}"
        
        cur.execute("""
            INSERT INTO transportdienstleister (name, typ, adresse, ansprechpartner)
            VALUES (%s, %s, %s, %s)
        """, (name, typ, adresse, ansprechpartner))
    
    conn.commit()
    log_metadata(conn, "transportdienstleister", "stammdaten_generator.generate_transportdienstleister")
    cur.close()
    print(f"{anzahl} Transportdienstleister erstellt")

# Produkte generieren
def generate_produkte(conn, anzahl=8):
    cur = conn.cursor()
    
    for i in range(anzahl):
        name = random.choice(produkt_namen)
        kategorie = random.choice(produkt_kategorien)
        
        cur.execute("""
            INSERT INTO produkt (name, kategorie)
            VALUES (%s, %s)
        """, (name, kategorie))
    
    conn.commit()
    log_metadata(conn, "produkt", "stammdaten_generator.generate_produkte")
    cur.close()
    print(f"{anzahl} Produkte erstellt")

def generate_plantagen(conn, anzahl=5):
    cur = conn.cursor()
    # Hole Partnerunternehmen-IDs
    cur.execute("SELECT partnerId FROM partnerunternehmen")
    partner_ids = [row[0] for row in cur.fetchall()]
    for i in range(anzahl):
        partnerId = random.choice(partner_ids)
        name = f"Plantage {i+1}"
        standort = random.choice(adressen)
        cur.execute("""
            INSERT INTO plantage (partnerId, name, standort)
            VALUES (%s, %s, %s)
        """, (partnerId, name, standort))
    conn.commit()
    log_metadata(conn, "plantage", "stammdaten_generator.generate_plantagen")
    cur.close()
    print(f"{anzahl} Plantagen erstellt")

def generate_qcstellen(conn, anzahl=3):
    cur = conn.cursor()
    cur.execute("SELECT partnerId FROM partnerunternehmen")
    partner_ids = [row[0] for row in cur.fetchall()]
    for i in range(anzahl):
        partnerId = random.choice(partner_ids)
        name = f"QC-Stelle {i+1}"
        standort = random.choice(adressen)
        cur.execute("""
            INSERT INTO qcstelle (partnerId, name, standort)
            VALUES (%s, %s, %s)
        """, (partnerId, name, standort))
    conn.commit()
    log_metadata(conn, "qcstelle", "stammdaten_generator.generate_qcstellen")
    cur.close()
    print(f"{anzahl} QC-Stellen erstellt")

def generate_hafenlager(conn, anzahl=2):
    cur = conn.cursor()
    cur.execute("SELECT partnerId FROM partnerunternehmen")
    partner_ids = [row[0] for row in cur.fetchall()]
    for i in range(anzahl):
        partnerId = random.choice(partner_ids)
        name = f"Hafenlager {i+1}"
        standort = random.choice(adressen)
        cur.execute("""
            INSERT INTO hafenlager (partnerId, name, standort)
            VALUES (%s, %s, %s)
        """, (partnerId, name, standort))
    conn.commit()
    log_metadata(conn, "hafenlager", "stammdaten_generator.generate_hafenlager")
    cur.close()
    print(f"{anzahl} Hafenlager erstellt")

# Hauptfunktion
def main():
    conn = get_db_connection()
    print("Generiere Stammdaten...")

    generate_partnerunternehmen(conn, 10)
    generate_transportdienstleister(conn, 5)
    generate_produkte(conn, 8)
    generate_plantagen(conn, 5)
    generate_qcstellen(conn, 3)
    generate_hafenlager(conn, 2)

    conn.close()
    print("Stammdaten erfolgreich generiert!")

if __name__ == "__main__":
    main()