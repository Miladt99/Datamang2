import sqlite3
from pymongo import MongoClient
import random
from datetime import datetime, timedelta


def log_metadata(cursor, table_name, source):
    cursor.execute(
        "INSERT INTO metadata (table_name, created_at, source) VALUES (?, ?, ?)",
        (table_name, datetime.now(), source),
    )

def insert_data():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    # Partnerunternehmen
    cursor.execute("INSERT INTO partnerunternehmen (name, typ, adresse, ansprechpartner) VALUES (?, ?, ?, ?)",
                   ("Banana Republic GmbH", "Plantage", "Plantagenweg 1, Bananien", "Carlos Frucht"))

    partner_id = cursor.lastrowid

    # Produkt: Banane
    cursor.execute("INSERT INTO produkt (name, kategorie) VALUES (?, ?)",
                   ("Banane", "Obst"))
    produkt_id = cursor.lastrowid

    # Plantage
    cursor.execute("INSERT INTO plantage (partnerId, name, standort) VALUES (?, ?, ?)",
                   (partner_id, "Plantage Süd", "Tropeninsel 9"))
    plantage_id = cursor.lastrowid

    # Ernten (10 Tage simulieren)
    for i in range(10):
        datum = datetime.now() - timedelta(days=i)
        menge = round(random.uniform(500, 1000), 2)
        cursor.execute("INSERT INTO ernte (plantageId, produktId, erntedatum, mengekg) VALUES (?, ?, ?, ?)",
                       (plantage_id, produkt_id, datum.date(), menge))
    log_metadata(cursor, "partnerunternehmen", "generate_data.insert_data")
    log_metadata(cursor, "produkt", "generate_data.insert_data")
    log_metadata(cursor, "plantage", "generate_data.insert_data")
    log_metadata(cursor, "ernte", "generate_data.insert_data")
    conn.commit()
    conn.close()


def insert_qc_data():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    # QC-Stelle anlegen
    cursor.execute("INSERT INTO qcstelle (partnerId, name, standort) VALUES (?, ?, ?)",
                   (1, "QC Tropic GmbH", "Hafenstraße 12"))  # dummy partnerId
    qc_id = cursor.lastrowid

    # Alle Ernten abrufen
    cursor.execute("SELECT ernteId, erntedatum FROM ernte")
    ernten = cursor.fetchall()

    for ernteId, erntedatum in ernten:
        qualitaet = random.choice(["A", "B", "C"])
        freigabe = random.choice(["freigegeben", "nicht freigegeben"])
        probenahmedatum = datetime.strptime(erntedatum, "%Y-%m-%d").date()

        # Probe
        cursor.execute("INSERT INTO qcprobe (ernteId, qcId, probenahmedatum, qualitaet) VALUES (?, ?, ?, ?)",
                       (ernteId, qc_id, probenahmedatum, qualitaet))
        probe_id = cursor.lastrowid

        # Freigabe
        cursor.execute("INSERT INTO qcfreigabe (probeId, freigabedatum, status) VALUES (?, ?, ?)",
                       (probe_id, probenahmedatum + timedelta(days=1), freigabe))
    log_metadata(cursor, "qcstelle", "generate_data.insert_qc_data")
    log_metadata(cursor, "qcprobe", "generate_data.insert_qc_data")
    log_metadata(cursor, "qcfreigabe", "generate_data.insert_qc_data")
    conn.commit()
    conn.close()



def insert_hafen_data():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    # Dummy-Hafenlager anlegen (nur einmal)
    cursor.execute("INSERT INTO hafenlager (partnerId, name, standort) VALUES (?, ?, ?)",
                   (1, "Hafenlager BananaPort", "Banania-Hafen 1"))
    hafen_id = cursor.lastrowid

    # Alle freigegebenen Ernten ermitteln
    cursor.execute("""
        SELECT f.freigabeId, p.probeId, e.mengekg, e.produktId
        FROM qcfreigabe f
        JOIN qcprobe p ON f.probeId = p.probeId
        JOIN ernte e ON p.ernteId = e.ernteId
        WHERE f.status = 'freigegeben'
    """)
    daten = cursor.fetchall()

    bestand = {}

    for freigabeId, _, menge, produktId in daten:
        ankunft = datetime.now().date()
        cursor.execute("""
            INSERT INTO hafenwareneingang (freigabeId, hafenId, ankunftsdatum, mengekg)
            VALUES (?, ?, ?, ?)""",
            (freigabeId, hafen_id, ankunft, menge))

        # Bestand aufbauen (akkumulieren)
        key = (hafen_id, produktId)
        bestand[key] = bestand.get(key, 0) + menge

    # Bestandstabelle updaten
    for (hafenId, produktId), menge in bestand.items():
        cursor.execute("""
            INSERT INTO hafenbestand (hafenId, produktId, mengekg)
            VALUES (?, ?, ?)""",
            (hafenId, produktId, menge))

        conn.commit()
    log_metadata(cursor, "hafenlager", "generate_data.insert_hafen_data")
    log_metadata(cursor, "hafenwareneingang", "generate_data.insert_hafen_data")
    log_metadata(cursor, "hafenbestand", "generate_data.insert_hafen_data")
    conn.commit()
    conn.close()



def insert_dc_data():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    # Distributionszentrum anlegen
    cursor.execute("INSERT INTO dcstandort (partnerId, name, standort) VALUES (?, ?, ?)",
                   (1, "DC Zentrum Nord", "Industriestraße 99"))
    dc_id = cursor.lastrowid

    # Alle Hafenbestände holen
    cursor.execute("SELECT bestandId, produktId, mengekg FROM hafenbestand")
    hafenbestaende = cursor.fetchall()

    dcbestand = {}

    for bestandId, produktId, menge in hafenbestaende:
        # Eingang in DC
        cursor.execute("""
            INSERT INTO dcwareneingang (bestandId, dcId, ankunftsdatum, mengekg)
            VALUES (?, ?, ?, ?)
        """, (bestandId, dc_id, datetime.now().date(), menge))

        # Bestand aufsummieren
        key = (dc_id, produktId)
        dcbestand[key] = dcbestand.get(key, 0) + menge

    # DC-Bestandstabelle füllen
    for (dcId, produktId), menge in dcbestand.items():
        cursor.execute("""
            INSERT INTO dcbestand (dcId, produktId, mengekg)
            VALUES (?, ?, ?)
        """, (dcId, produktId, menge))
    log_metadata(cursor, "dcstandort", "generate_data.insert_dc_data")
    log_metadata(cursor, "dcwareneingang", "generate_data.insert_dc_data")
    log_metadata(cursor, "dcbestand", "generate_data.insert_dc_data")
    conn.commit()
    conn.close()


def insert_pos_data():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    # POS-Standort anlegen
    cursor.execute("INSERT INTO posstandort (partnerId, name, adresse) VALUES (?, ?, ?)",
                   (1, "Supermarkt Banano", "Innenstadt 42"))
    pos_id = cursor.lastrowid

    # DC-Bestand holen
    cursor.execute("SELECT dcbestandId, produktId, mengekg FROM dcbestand")
    dc_bestand = cursor.fetchall()

    posbestand = {}

    for dcbestandId, produktId, menge in dc_bestand:
        # POS Wareneingang
        cursor.execute("""
            INSERT INTO poswareneingang (dcbestandId, posId, ankunftsdatum, mengekg)
            VALUES (?, ?, ?, ?)
        """, (dcbestandId, pos_id, datetime.now().date(), menge))

        # POS Bestand
        key = (pos_id, produktId)
        posbestand[key] = posbestand.get(key, 0) + menge

    # POS-Bestand speichern
    for (posId, produktId), menge in posbestand.items():
        cursor.execute("""
            INSERT INTO posbestand (posId, produktId, mengekg)
            VALUES (?, ?, ?)
        """, (posId, produktId, menge))
    # Verkaufsdaten (10 Verkäufe simulieren)
    cursor.execute("SELECT posbestandId, mengekg FROM posbestand")
    alle_bestaende = cursor.fetchall()

    for posbestandId, bestand in alle_bestaende:
        verkauft_total = 0.0
        for i in range(10):
            verkaufsdatum = datetime.now().date() - timedelta(days=random.randint(0, 5))
            verkauft = round(random.uniform(1.0, 10.0), 2)
            if verkauft_total + verkauft > bestand:
                break  # nicht überverkaufen
            verkauft_total += verkauft
            cursor.execute("""
                INSERT INTO posverkauf (posbestandId, verkaufsdatum, verkauftemengekg)
                VALUES (?, ?, ?)
            """, (posbestandId, verkaufsdatum, verkauft))

        # optional: Bestand nach Verkauf anpassen (Simulation)
        cursor.execute("UPDATE posbestand SET mengekg = ? WHERE posbestandId = ?",
                       (bestand - verkauft_total, posbestandId))

    log_metadata(cursor, "posstandort", "generate_data.insert_pos_data")
    log_metadata(cursor, "poswareneingang", "generate_data.insert_pos_data")
    log_metadata(cursor, "posbestand", "generate_data.insert_pos_data")
    log_metadata(cursor, "posverkauf", "generate_data.insert_pos_data")
    conn.commit()
    conn.close()


def insert_transportauftraege():
    conn = sqlite3.connect("dma_bananen.db")
    cursor = conn.cursor()

    # Dienstleister prüfen oder erstellen
    cursor.execute("SELECT dienstleisterId FROM transportdienstleister WHERE name = ?", ("TropicLogistics",))
    result = cursor.fetchone()
    if result:
        dienstleister_id = result[0]
    else:
        cursor.execute("INSERT INTO transportdienstleister (name, typ, adresse, ansprechpartner) VALUES (?, ?, ?, ?)",
                       ("TropicLogistics", "LKW", "Transweg 5", "Maria Banana"))
        dienstleister_id = cursor.lastrowid

    now = datetime.now()

    # DC prüfen
    cursor.execute("SELECT dcId FROM dcstandort")
    dc = cursor.fetchone()
    if dc is None:
        print("⚠️ Kein DC gefunden.")
        conn.close()
        return
    dcId = dc[0]

    # POS prüfen
    cursor.execute("SELECT posId FROM posstandort")
    pos = cursor.fetchone()
    if pos is None:
        print("⚠️ Kein POS gefunden.")
        conn.close()
        return
    posId = pos[0]

    for i in range(5):
        abfahrt = now - timedelta(days=i + 2)
        ankunft = abfahrt + timedelta(hours=6)
        transportmittel = random.choice(["LKW", "Bahn", "Schiff", "Flugzeug"])

        cursor.execute("""
            INSERT INTO transportauftrag (
                dienstleisterId, startorttyp, startortId, zielorttyp, zielortId,
                abfahrtszeit, ankunftszeit, transportmittel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (dienstleister_id, "DC", dcId, "POS", posId, abfahrt, ankunft, transportmittel))

   

    log_metadata(cursor, "transportdienstleister", "generate_data.insert_transportauftraege")
    log_metadata(cursor, "transportauftrag", "generate_data.insert_transportauftraege")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_data()