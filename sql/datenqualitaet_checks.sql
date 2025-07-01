-- Fehlende Werte in Partnerunternehmen
SELECT * FROM partnerunternehmen WHERE name IS NULL OR adresse IS NULL;

-- Ungültiger Typ in Partnerunternehmen
SELECT * FROM partnerunternehmen WHERE typ NOT IN ('Lieferant', 'Kunde', 'Logistikpartner', 'Hersteller', 'Händler');

-- Negative Mengen in Ernte
SELECT * FROM ernte WHERE mengekg < 0;

-- Fehlende Mengen in Ernte
SELECT * FROM ernte WHERE mengekg IS NULL;

-- Erntedatum in der Zukunft
SELECT * FROM ernte WHERE erntedatum > CURRENT_DATE;

-- Duplikate bei Partnerunternehmen
SELECT name, COUNT(*) FROM partnerunternehmen GROUP BY name HAVING COUNT(*) > 1;