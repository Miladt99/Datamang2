-- 1 Stammdaten
-- 1.1 Partnerunternehmen
CREATE TABLE partnerunternehmen (
    partnerId SERIAL PRIMARY KEY,
    name VARCHAR(255),
    typ VARCHAR(50),
    adresse TEXT,
    ansprechpartner VARCHAR(255)
);

-- 1.2 Transportdienstleister
CREATE TABLE transportdienstleister (
    dienstleisterId SERIAL PRIMARY KEY,
    name VARCHAR(255),
    typ VARCHAR(50),
    adresse TEXT,
    ansprechpartner VARCHAR(255)
);

-- 1.3 Produkt
CREATE TABLE produkt (
    produktId SERIAL PRIMARY KEY,
    name VARCHAR(255),
    kategorie VARCHAR(50)
);

-- 2 Operative Daten je Supply-Chain-Komponente
-- 2.1 Rohstoffabbau (Plantage)
CREATE TABLE plantage (
    plantageId SERIAL PRIMARY KEY,
    partnerId INT REFERENCES partnerunternehmen(partnerId),
    name VARCHAR(255),
    standort TEXT
);

CREATE TABLE ernte (
    ernteId SERIAL PRIMARY KEY,
    plantageId INT REFERENCES plantage(plantageId),
    produktId INT REFERENCES produkt(produktId),
    erntedatum DATE,
    mengekg DECIMAL(10,2)
);

-- 2.2 Qualitätskontrolle (QC)
CREATE TABLE qcstelle (
    qcId SERIAL PRIMARY KEY,
    partnerId INT REFERENCES partnerunternehmen(partnerId),
    name VARCHAR(255),
    standort TEXT
);

CREATE TABLE qcprobe (
    probeId SERIAL PRIMARY KEY,
    ernteId INT REFERENCES ernte(ernteId),
    qcId INT REFERENCES qcstelle(qcId),
    probenahmedatum DATE,
    qualitaet VARCHAR(10)
);

CREATE TABLE qcfreigabe (
    freigabeId SERIAL PRIMARY KEY,
    probeId INT REFERENCES qcprobe(probeId),
    freigabedatum DATE,
    status VARCHAR(50)
);

-- 2.3 Zentrallager am Hafen
CREATE TABLE hafenlager (
    hafenId SERIAL PRIMARY KEY,
    partnerId INT REFERENCES partnerunternehmen(partnerId),
    name VARCHAR(255),
    standort TEXT
);

CREATE TABLE hafenwareneingang (
    eingangId SERIAL PRIMARY KEY,
    freigabeId INT REFERENCES qcfreigabe(freigabeId),
    hafenId INT REFERENCES hafenlager(hafenId),
    ankunftsdatum DATE,
    mengekg DECIMAL(10,2)
);

CREATE TABLE hafenbestand (
    bestandId SERIAL PRIMARY KEY,
    hafenId INT REFERENCES hafenlager(hafenId),
    produktId INT REFERENCES produkt(produktId),
    mengekg DECIMAL(10,2)
);

-- 2.4 Zentrallager / Distributionszentrum (DC)
CREATE TABLE dcstandort (
    dcId SERIAL PRIMARY KEY,
    partnerId INT REFERENCES partnerunternehmen(partnerId),
    name VARCHAR(255),
    standort TEXT
);

CREATE TABLE dcwareneingang (
    dceingangId SERIAL PRIMARY KEY,
    bestandId INT REFERENCES hafenbestand(bestandId),
    dcId INT REFERENCES dcstandort(dcId),
    ankunftsdatum DATE,
    mengekg DECIMAL(10,2)
);

CREATE TABLE dcbestand (
    dcbestandId SERIAL PRIMARY KEY,
    dcId INT REFERENCES dcstandort(dcId),
    produktId INT REFERENCES produkt(produktId),
    mengekg DECIMAL(10,2)
);

-- 2.5 Point of Sale (POS)
CREATE TABLE posstandort (
    posId SERIAL PRIMARY KEY,
    partnerId INT REFERENCES partnerunternehmen(partnerId),
    name VARCHAR(255),
    adresse TEXT
);

CREATE TABLE poswareneingang (
    poseingangId SERIAL PRIMARY KEY,
    dcbestandId INT REFERENCES dcbestand(dcbestandId),
    posId INT REFERENCES posstandort(posId),
    ankunftsdatum DATE,
    mengekg DECIMAL(10,2)
);

CREATE TABLE posbestand (
    posbestandId SERIAL PRIMARY KEY,
    posId INT REFERENCES posstandort(posId),
    produktId INT REFERENCES produkt(produktId),
    mengekg DECIMAL(10,2)
);

CREATE TABLE posverkauf (
    verkaufId SERIAL PRIMARY KEY,
    posbestandId INT REFERENCES posbestand(posbestandId),
    verkaufsdatum DATE,
    verkauftemengekg DECIMAL(10,2)
);

-- 3 Transportaufträge
CREATE TABLE transportauftrag (
    transportId SERIAL PRIMARY KEY,
    dienstleisterId INT REFERENCES transportdienstleister(dienstleisterId),
    startorttyp VARCHAR(50),
    startortId INT,
    zielorttyp VARCHAR(50),
    zielortId INT,
    abfahrtszeit TIMESTAMP,
    ankunftszeit TIMESTAMP,
    transportmittel VARCHAR(50)
);

-- 3.1 Bestellschein
CREATE TABLE bestellschein (
    bestellscheinId SERIAL PRIMARY KEY,
    partnerId INT REFERENCES partnerunternehmen(partnerId),
    bestellscheinDatum DATE
);

-- 4 Metadaten zur Dokumentation von Datenherkünften
CREATE TABLE metadata (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255),
    created_at TIMESTAMP,
    source TEXT
);