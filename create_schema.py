import sqlite3

def create_tables():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS partnerunternehmen (
        partnerId INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        typ TEXT,
        adresse TEXT,
        ansprechpartner TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produkt (
        produktId INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        kategorie TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plantage (
        plantageId INTEGER PRIMARY KEY AUTOINCREMENT,
        partnerId INTEGER,
        name TEXT,
        standort TEXT,
        FOREIGN KEY (partnerId) REFERENCES partnerunternehmen(partnerId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ernte (
        ernteId INTEGER PRIMARY KEY AUTOINCREMENT,
        plantageId INTEGER,
        produktId INTEGER,
        erntedatum DATE,
        mengekg REAL,
        FOREIGN KEY (plantageId) REFERENCES plantage(plantageId),
        FOREIGN KEY (produktId) REFERENCES produkt(produktId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qcstelle (
        qcId INTEGER PRIMARY KEY AUTOINCREMENT,
        partnerId INTEGER,
        name TEXT,
        standort TEXT,
        FOREIGN KEY (partnerId) REFERENCES partnerunternehmen(partnerId)
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qcprobe (
        probeId INTEGER PRIMARY KEY AUTOINCREMENT,
        ernteId INTEGER,
        qcId INTEGER,
        probenahmedatum DATE,
        qualitaet TEXT,
        FOREIGN KEY (ernteId) REFERENCES ernte(ernteId),
        FOREIGN KEY (qcId) REFERENCES qcstelle(qcId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qcfreigabe (
        freigabeId INTEGER PRIMARY KEY AUTOINCREMENT,
        probeId INTEGER,
        freigabedatum DATE,
        status TEXT,
        FOREIGN KEY (probeId) REFERENCES qcprobe(probeId)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hafenlager (
        hafenId INTEGER PRIMARY KEY AUTOINCREMENT,
        partnerId INTEGER,
        name TEXT,
        standort TEXT,
        FOREIGN KEY (partnerId) REFERENCES partnerunternehmen(partnerId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hafenwareneingang (
        eingangId INTEGER PRIMARY KEY AUTOINCREMENT,
        freigabeId INTEGER,
        hafenId INTEGER,
        ankunftsdatum DATE,
        mengekg REAL,
        FOREIGN KEY (freigabeId) REFERENCES qcfreigabe(freigabeId),
        FOREIGN KEY (hafenId) REFERENCES hafenlager(hafenId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hafenbestand (
        bestandId INTEGER PRIMARY KEY AUTOINCREMENT,
        hafenId INTEGER,
        produktId INTEGER,
        mengekg REAL,
        FOREIGN KEY (hafenId) REFERENCES hafenlager(hafenId),
        FOREIGN KEY (produktId) REFERENCES produkt(produktId)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dcstandort (
        dcId INTEGER PRIMARY KEY AUTOINCREMENT,
        partnerId INTEGER,
        name TEXT,
        standort TEXT,
        FOREIGN KEY (partnerId) REFERENCES partnerunternehmen(partnerId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dcwareneingang (
        dceingangId INTEGER PRIMARY KEY AUTOINCREMENT,
        bestandId INTEGER,
        dcId INTEGER,
        ankunftsdatum DATE,
        mengekg REAL,
        FOREIGN KEY (bestandId) REFERENCES hafenbestand(bestandId),
        FOREIGN KEY (dcId) REFERENCES dcstandort(dcId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dcbestand (
        dcbestandId INTEGER PRIMARY KEY AUTOINCREMENT,
        dcId INTEGER,
        produktId INTEGER,
        mengekg REAL,
        FOREIGN KEY (dcId) REFERENCES dcstandort(dcId),
        FOREIGN KEY (produktId) REFERENCES produkt(produktId)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posstandort (
        posId INTEGER PRIMARY KEY AUTOINCREMENT,
        partnerId INTEGER,
        name TEXT,
        adresse TEXT,
        FOREIGN KEY (partnerId) REFERENCES partnerunternehmen(partnerId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS poswareneingang (
        poseingangId INTEGER PRIMARY KEY AUTOINCREMENT,
        dcbestandId INTEGER,
        posId INTEGER,
        ankunftsdatum DATE,
        mengekg REAL,
        FOREIGN KEY (dcbestandId) REFERENCES dcbestand(dcbestandId),
        FOREIGN KEY (posId) REFERENCES posstandort(posId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posbestand (
        posbestandId INTEGER PRIMARY KEY AUTOINCREMENT,
        posId INTEGER,
        produktId INTEGER,
        mengekg REAL,
        FOREIGN KEY (posId) REFERENCES posstandort(posId),
        FOREIGN KEY (produktId) REFERENCES produkt(produktId)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posverkauf (
        verkaufId INTEGER PRIMARY KEY AUTOINCREMENT,
        posbestandId INTEGER,
        verkaufsdatum DATE,
        verkauftemengekg REAL,
        FOREIGN KEY (posbestandId) REFERENCES posbestand(posbestandId)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transportauftrag (
        transportId INTEGER PRIMARY KEY AUTOINCREMENT,
        dienstleisterId INTEGER,
        startorttyp TEXT,
        startortId INTEGER,
        zielorttyp TEXT,
        zielortId INTEGER,
        abfahrtszeit TIMESTAMP,
        ankunftszeit TIMESTAMP,
        transportmittel TEXT,
        FOREIGN KEY (dienstleisterId) REFERENCES transportdienstleister(dienstleisterId)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT,
        created_at TIMESTAMP,
        source TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bestellschein (
        bestellscheinId INTEGER PRIMARY KEY AUTOINCREMENT,
        partnerId INTEGER,
        bestellscheinDatum DATE,
        FOREIGN KEY (partnerId) REFERENCES partnerunternehmen(partnerId)
    )
    """)

    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
