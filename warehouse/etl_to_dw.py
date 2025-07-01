import sqlite3
from datetime import datetime

SOURCE_DB = '../dma_bananen.db'
TARGET_DB = 'dma_dw.db'


def get_connection(path):
    return sqlite3.connect(path)


def load_dimensions(src, dw):
    s = src.cursor()
    d = dw.cursor()

    for row in s.execute("SELECT partnerId, name, typ, adresse, ansprechpartner FROM partnerunternehmen"):
        d.execute(
            "INSERT OR IGNORE INTO dim_partnerunternehmen VALUES (?, ?, ?, ?, ?)",
            row
        )

    for row in s.execute("SELECT produktId, name, kategorie FROM produkt"):
        d.execute(
            "INSERT OR IGNORE INTO dim_product VALUES (?, ?, ?)",
            row
        )

    for row in s.execute("SELECT plantageId, partnerId, name, standort FROM plantage"):
        d.execute(
            "INSERT OR IGNORE INTO dim_plantage VALUES (?, ?, ?, ?)",
            row
        )

    for row in s.execute("SELECT qcId, partnerId, name, standort FROM qcstelle"):
        d.execute(
            "INSERT OR IGNORE INTO dim_qcstelle VALUES (?, ?, ?, ?)",
            row
        )

    for row in s.execute("SELECT hafenId, partnerId, name, standort FROM hafenlager"):
        d.execute(
            "INSERT OR IGNORE INTO dim_hafenlager VALUES (?, ?, ?, ?)",
            row
        )

    for row in s.execute("SELECT dcId, partnerId, name, standort FROM dcstandort"):
        d.execute(
            "INSERT OR IGNORE INTO dim_dcstandort VALUES (?, ?, ?, ?)",
            row
        )

    for row in s.execute("SELECT posId, partnerId, name, adresse FROM posstandort"):
        d.execute(
            "INSERT OR IGNORE INTO dim_posstandort VALUES (?, ?, ?, ?)",
            row
        )

    for row in s.execute("SELECT dienstleisterId, name, typ, adresse, ansprechpartner FROM transportdienstleister"):
        d.execute(
            "INSERT OR IGNORE INTO dim_dienstleister VALUES (?, ?, ?, ?, ?)",
            row
        )

    dw.commit()


def get_date_id(cursor, dt):
    date_str = dt.strftime('%Y-%m-%d')
    cursor.execute("SELECT date_id FROM dim_date WHERE full_date = ?", (date_str,))
    res = cursor.fetchone()
    if res:
        return res[0]
    date_id = int(dt.strftime('%Y%m%d'))
    cursor.execute(
        "INSERT INTO dim_date (date_id, full_date, year, month, day, day_of_week) VALUES (?, ?, ?, ?, ?, ?)",
        (date_id, date_str, dt.year, dt.month, dt.day, dt.weekday())
    )
    return date_id


def load_facts(src, dw):
    s = src.cursor()
    d = dw.cursor()

    # fact_ernte
    for ernte_id, plantage_id, produkt_id, erntedatum, menge in s.execute(
        "SELECT ernteId, plantageId, produktId, erntedatum, mengekg FROM ernte"
    ):
        date_id = get_date_id(d, datetime.fromisoformat(erntedatum))
        d.execute(
            "INSERT OR IGNORE INTO fact_ernte VALUES (?, ?, ?, ?, ?)",
            (ernte_id, plantage_id, produkt_id, date_id, menge)
        )

    # fact_qcprobe
    query = """
        SELECT p.probeId, p.ernteId, p.qcId, p.probenahmedatum, p.qualitaet,
               f.status, f.freigabedatum
        FROM qcprobe p
        LEFT JOIN qcfreigabe f ON p.probeId = f.probeId
    """
    for row in s.execute(query):
        probe_id, ernte_id, qc_id, datum, qualitaet, status, freidatum = row
        date_id = get_date_id(d, datetime.fromisoformat(datum))
        d.execute(
            "INSERT OR IGNORE INTO fact_qcprobe VALUES (?, ?, ?, ?, ?, ?)",
            (probe_id, ernte_id, qc_id, date_id, qualitaet, status)
        )

    # hafen eingang
    for eingang_id, freigabe_id, hafen_id, ankunft, menge in s.execute(
        "SELECT eingangId, freigabeId, hafenId, ankunftsdatum, mengekg FROM hafenwareneingang"
    ):
        produkt = s.execute(
            "SELECT e.produktId FROM qcfreigabe f JOIN qcprobe p ON f.probeId = p.probeId JOIN ernte e ON p.ernteId = e.ernteId WHERE f.freigabeId = ?",
            (freigabe_id,)
        ).fetchone()
        produkt_id = produkt[0] if produkt else None
        date_id = get_date_id(d, datetime.fromisoformat(ankunft))
        d.execute(
            "INSERT OR IGNORE INTO fact_hafen_eingang VALUES (?, ?, ?, ?, ?, ?)",
            (eingang_id, freigabe_id, hafen_id, produkt_id, date_id, menge)
        )

    # dc eingang
    for eid, bestand_id, dc_id, ankunft, menge in s.execute(
        "SELECT dceingangId, bestandId, dcId, ankunftsdatum, mengekg FROM dcwareneingang"
    ):
        prod_row = s.execute("SELECT produktId FROM hafenbestand WHERE bestandId = ?", (bestand_id,)).fetchone()
        produkt_id = prod_row[0] if prod_row else None
        date_id = get_date_id(d, datetime.fromisoformat(ankunft))
        d.execute(
            "INSERT OR IGNORE INTO fact_dc_eingang VALUES (?, ?, ?, ?, ?)",
            (eid, dc_id, produkt_id, date_id, menge)
        )

    # pos eingang
    for eid, bestand_id, pos_id, ankunft, menge in s.execute(
        "SELECT poseingangId, dcbestandId, posId, ankunftsdatum, mengekg FROM poswareneingang"
    ):
        prod_row = s.execute("SELECT produktId FROM dcbestand WHERE dcbestandId = ?", (bestand_id,)).fetchone()
        produkt_id = prod_row[0] if prod_row else None
        date_id = get_date_id(d, datetime.fromisoformat(ankunft))
        d.execute(
            "INSERT OR IGNORE INTO fact_pos_eingang VALUES (?, ?, ?, ?, ?)",
            (eid, pos_id, produkt_id, date_id, menge)
        )

    # verkauf
    for verkauf_id, posbestand_id, datum, menge in s.execute(
        "SELECT verkaufId, posbestandId, verkaufsdatum, verkauftemengekg FROM posverkauf"
    ):
        prod_row = s.execute("SELECT produktId, posId FROM posbestand WHERE posbestandId = ?", (posbestand_id,)).fetchone()
        if not prod_row:
            continue
        produkt_id, pos_id = prod_row
        date_id = get_date_id(d, datetime.fromisoformat(datum))
        d.execute(
            "INSERT OR IGNORE INTO fact_pos_verkauf VALUES (?, ?, ?, ?, ?)",
            (verkauf_id, pos_id, produkt_id, date_id, menge)
        )

    # transport
    for row in s.execute(
        "SELECT transportId, dienstleisterId, startorttyp, startortId, zielorttyp, zielortId, abfahrtszeit, ankunftszeit, transportmittel FROM transportauftrag"
    ):
        (tid, dl_id, st_typ, st_id, zi_typ, zi_id, abf, ank, mittel) = row
        start_date = get_date_id(d, datetime.fromisoformat(abf))
        ziel_date = get_date_id(d, datetime.fromisoformat(ank))
        d.execute(
            "INSERT OR IGNORE INTO fact_transport VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (tid, dl_id, st_typ, st_id, zi_typ, zi_id, start_date, ziel_date, mittel)
        )

    dw.commit()


def run():
    src = get_connection(SOURCE_DB)
    dw = get_connection(TARGET_DB)
    with open('create_dw_schema.sql', 'r', encoding='utf-8') as f:
        dw.executescript(f.read())
    load_dimensions(src, dw)
    load_facts(src, dw)
    dw.close()
    src.close()


if __name__ == '__main__':
    run()