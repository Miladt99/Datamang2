import psycopg2
import pandas as pd
import os

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    database=os.getenv("POSTGRES_DB", "supplychain"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "password"),
)

# Partnerunternehmen prüfen
df_partner = pd.read_sql("SELECT * FROM partnerunternehmen", conn)
print("Fehlende Namen/Adressen:")
print(df_partner[df_partner['name'].isnull() | df_partner['adresse'].isnull()])

print("\nUngültiger Typ:")
print(df_partner[~df_partner['typ'].isin(['Lieferant', 'Kunde', 'Logistikpartner', 'Hersteller', 'Händler'])])

# Ernte prüfen
df_ernte = pd.read_sql("SELECT * FROM ernte", conn)
print("\nNegative Mengen:")
print(df_ernte[df_ernte['mengekg'] < 0])

print("\nFehlende Mengen:")
print(df_ernte[df_ernte['mengekg'].isnull()])

print("\nErntedatum in der Zukunft:")
print(df_ernte[pd.to_datetime(df_ernte['erntedatum']) > pd.Timestamp.today()])

conn.close()