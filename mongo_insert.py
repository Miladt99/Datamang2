from pymongo import MongoClient
from datetime import datetime
import random

def insert_bestellscheine():
    # Verbindung zur lokalen MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["dma_bananen"]
    collection = db["bestellscheine"]

    # Beispiel-Produktnamen
    produkte = ["Banane Premium", "Banane Bio", "Babybananen"]

    # Beispielkunden
    kunden = ["Edeka Nord", "Rewe Süd", "Fruchtimport AG", "Bananenladen24"]

    # Bestellscheine generieren
    for i in range(10):
        produkt = random.choice(produkte)
        menge = round(random.uniform(100, 1000), 2)
        kunde = random.choice(kunden)
        datum = datetime.now().strftime("%Y-%m-%d")

        bestellung = {
            "kunde": kunde,
            "produkte": [
                {
                    "name": produkt,
                    "menge_kg": menge,
                    "einheit": "kg"
                }
            ],
            "gesamtmenge_kg": menge,
            "lieferadresse": f"{kunde} Hauptlager",
            "bestelldatum": datum,
            "freitext": "Expresslieferung bitte"
        }

        collection.insert_one(bestellung)

    print("✅ 10 Bestellscheine in MongoDB eingefügt.")
