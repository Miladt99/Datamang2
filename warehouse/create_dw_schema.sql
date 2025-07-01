-- Star schema for banana supply chain data warehouse
-- Dimension tables
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER
);

CREATE TABLE IF NOT EXISTS dim_partnerunternehmen (
    partner_id INTEGER PRIMARY KEY,
    name TEXT,
    typ TEXT,
    adresse TEXT,
    ansprechpartner TEXT
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    kategorie TEXT
);

CREATE TABLE IF NOT EXISTS dim_plantage (
    plantage_id INTEGER PRIMARY KEY,
    partner_id INTEGER,
    name TEXT,
    standort TEXT,
    FOREIGN KEY(partner_id) REFERENCES dim_partnerunternehmen(partner_id)
);

CREATE TABLE IF NOT EXISTS dim_qcstelle (
    qc_id INTEGER PRIMARY KEY,
    partner_id INTEGER,
    name TEXT,
    standort TEXT,
    FOREIGN KEY(partner_id) REFERENCES dim_partnerunternehmen(partner_id)
);

CREATE TABLE IF NOT EXISTS dim_hafenlager (
    hafen_id INTEGER PRIMARY KEY,
    partner_id INTEGER,
    name TEXT,
    standort TEXT,
    FOREIGN KEY(partner_id) REFERENCES dim_partnerunternehmen(partner_id)
);

CREATE TABLE IF NOT EXISTS dim_dcstandort (
    dc_id INTEGER PRIMARY KEY,
    partner_id INTEGER,
    name TEXT,
    standort TEXT,
    FOREIGN KEY(partner_id) REFERENCES dim_partnerunternehmen(partner_id)
);

CREATE TABLE IF NOT EXISTS dim_posstandort (
    pos_id INTEGER PRIMARY KEY,
    partner_id INTEGER,
    name TEXT,
    adresse TEXT,
    FOREIGN KEY(partner_id) REFERENCES dim_partnerunternehmen(partner_id)
);

CREATE TABLE IF NOT EXISTS dim_dienstleister (
    dienstleister_id INTEGER PRIMARY KEY,
    name TEXT,
    typ TEXT,
    adresse TEXT,
    ansprechpartner TEXT
);

-- Fact tables
CREATE TABLE IF NOT EXISTS fact_ernte (
    ernte_id INTEGER PRIMARY KEY,
    plantage_id INTEGER,
    product_id INTEGER,
    date_id INTEGER,
    mengekg REAL,
    FOREIGN KEY(plantage_id) REFERENCES dim_plantage(plantage_id),
    FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_qcprobe (
    probe_id INTEGER PRIMARY KEY,
    ernte_id INTEGER,
    qc_id INTEGER,
    date_id INTEGER,
    qualitaet TEXT,
    freigabe_status TEXT,
    FOREIGN KEY(ernte_id) REFERENCES fact_ernte(ernte_id),
    FOREIGN KEY(qc_id) REFERENCES dim_qcstelle(qc_id),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_hafen_eingang (
    eingang_id INTEGER PRIMARY KEY,
    freigabe_id INTEGER,
    hafen_id INTEGER,
    product_id INTEGER,
    date_id INTEGER,
    mengekg REAL,
    FOREIGN KEY(hafen_id) REFERENCES dim_hafenlager(hafen_id),
    FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_dc_eingang (
    dceingang_id INTEGER PRIMARY KEY,
    dc_id INTEGER,
    product_id INTEGER,
    date_id INTEGER,
    mengekg REAL,
    FOREIGN KEY(dc_id) REFERENCES dim_dcstandort(dc_id),
    FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_pos_eingang (
    poseingang_id INTEGER PRIMARY KEY,
    pos_id INTEGER,
    product_id INTEGER,
    date_id INTEGER,
    mengekg REAL,
    FOREIGN KEY(pos_id) REFERENCES dim_posstandort(pos_id),
    FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_pos_verkauf (
    verkauf_id INTEGER PRIMARY KEY,
    pos_id INTEGER,
    product_id INTEGER,
    date_id INTEGER,
    verkauftemengekg REAL,
    FOREIGN KEY(pos_id) REFERENCES dim_posstandort(pos_id),
    FOREIGN KEY(product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_transport (
    transport_id INTEGER PRIMARY KEY,
    dienstleister_id INTEGER,
    startorttyp TEXT,
    startort_id INTEGER,
    zielorttyp TEXT,
    zielort_id INTEGER,
    start_date_id INTEGER,
    ziel_date_id INTEGER,
    transportmittel TEXT,
    FOREIGN KEY(dienstleister_id) REFERENCES dim_dienstleister(dienstleister_id),
    FOREIGN KEY(start_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY(ziel_date_id) REFERENCES dim_date(date_id)
);