import psycopg2
import os
import random
from datetime import datetime, timedelta

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5433"),
        database=os.getenv("POSTGRES_DB", "supplychain"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
    )

def get_ids(cur, table, id_col):
    cur.execute(f"SELECT {id_col} FROM {table}")
    return [row[0] for row in cur.fetchall()]

def generate_ernte(conn, anzahl=20, fehlerquote=0.2):
    cur = conn.cursor()
    plantage_ids = get_ids(cur, "plantage", "plantageId")
    produkt_ids = get_ids(cur, "produkt", "produktId")
    for _ in range(anzahl):
        plantageId = random.choice(plantage_ids)
        produktId = random.choice(produkt_ids)
        erntedatum = datetime.now() - timedelta(days=random.randint(0, 30))
        mengekg = round(random.uniform(100, 1000), 2)

        # Fehler einbauen
        if random.random() < fehlerquote:
            fehlerart = random.choice(["negativ", "leer", "falsches_datum"])
            if fehlerart == "negativ":
                mengekg = -abs(mengekg)
            elif fehlerart == "leer":
                mengekg = None
            elif fehlerart == "falsches_datum":
                erntedatum = datetime.now() + timedelta(days=365)  # Datum in der Zukunft

        cur.execute("""
            INSERT INTO ernte (plantageId, produktId, erntedatum, mengekg)
            VALUES (%s, %s, %s, %s)
        """, (plantageId, produktId, erntedatum.date(), mengekg))
    conn.commit()
    cur.close()
    print(f"{anzahl} Ernten (inkl. fehlerhafte) generiert.")
    print(f"{anzahl} Ernten generiert.")

def generate_qcprobe(conn, anzahl=15):
    cur = conn.cursor()
    ernte_ids = get_ids(cur, "ernte", "ernteId")
    qc_ids = get_ids(cur, "qcstelle", "qcId")
    for _ in range(anzahl):
        ernteId = random.choice(ernte_ids)
        qcId = random.choice(qc_ids)
        probenahmedatum = datetime.now() - timedelta(days=random.randint(0, 30))
        qualitaet = random.choice(["A", "B", "C"])
        cur.execute("""
            INSERT INTO qcprobe (ernteId, qcId, probenahmedatum, qualitaet)
            VALUES (%s, %s, %s, %s)
        """, (ernteId, qcId, probenahmedatum.date(), qualitaet))
    conn.commit()
    cur.close()
    print(f"{anzahl} QC-Proben generiert.")

def generate_qcfreigabe(conn, anzahl=10):
    cur = conn.cursor()
    probe_ids = get_ids(cur, "qcprobe", "probeId")
    for _ in range(anzahl):
        probeId = random.choice(probe_ids)
        freigabedatum = datetime.now() - timedelta(days=random.randint(0, 30))
        status = random.choice(["freigegeben", "gesperrt"])
        cur.execute("""
            INSERT INTO qcfreigabe (probeId, freigabedatum, status)
            VALUES (%s, %s, %s)
        """, (probeId, freigabedatum.date(), status))
    conn.commit()
    cur.close()
    print(f"{anzahl} QC-Freigaben generiert.")

def generate_hafenwareneingang(conn, anzahl=10):
    cur = conn.cursor()
    freigabe_ids = get_ids(cur, "qcfreigabe", "freigabeId")
    hafen_ids = get_ids(cur, "hafenlager", "hafenId")
    for _ in range(anzahl):
        freigabeId = random.choice(freigabe_ids)
        hafenId = random.choice(hafen_ids)
        ankunftsdatum = datetime.now() - timedelta(days=random.randint(0, 30))
        mengekg = round(random.uniform(100, 1000), 2)
        cur.execute("""
            INSERT INTO hafenwareneingang (freigabeId, hafenId, ankunftsdatum, mengekg)
            VALUES (%s, %s, %s, %s)
        """, (freigabeId, hafenId, ankunftsdatum.date(), mengekg))
    conn.commit()
    cur.close()
    print(f"{anzahl} Hafenwareneingänge generiert.")

def generate_posverkauf(conn, anzahl=10):
    cur = conn.cursor()
    posbestand_ids = get_ids(cur, "posbestand", "posbestandId")
    for _ in range(anzahl):
        posbestandId = random.choice(posbestand_ids)
        verkaufsdatum = datetime.now() - timedelta(days=random.randint(0, 30))
        verkauftemengekg = round(random.uniform(1, 100), 2)
        cur.execute("""
            INSERT INTO posverkauf (posbestandId, verkaufsdatum, verkauftemengekg)
            VALUES (%s, %s, %s)
        """, (posbestandId, verkaufsdatum.date(), verkauftemengekg))
    conn.commit()
    cur.close()
    print(f"{anzahl} POS-Verkäufe generiert.")

def main():
    conn = get_db_connection()
    print("Generiere Bewegungsdaten...")

    # Hier kannst du die Reihenfolge und Anzahl anpassen
    generate_ernte(conn, 20)
    generate_qcprobe(conn, 15)
    generate_qcfreigabe(conn, 10)
    generate_hafenwareneingang(conn, 10)
    # ... weitere Generatoren für andere Tabellen nach Bedarf ergänzen

    conn.close()
    print("Bewegungsdaten erfolgreich generiert!")

if __name__ == "__main__":
    main()