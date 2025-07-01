from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# Verbindung zu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['supplychain']
collection = db['bestellscheine']

# Beispiel-Stammdaten (abweichend von SQL)
kunden_namen = [
    "Müller GmbH", "Schmidt AG", "Beispiel & Co", "Testkunde KG", "Fiktiv AG"
]
produkte = [
    {"name": "Bio-Bananen", "artikelnummer": "B1001"},
    {"name": "Premium-Bananen", "artikelnummer": "B1002"},
    {"name": "Tropenmix", "artikelnummer": "T2001"},
    {"name": "Exotenbox", "artikelnummer": "E3001"}
]

def generate_bestellschein(nr):
    kunde = random.choice(kunden_namen)
    datum = datetime.now() - timedelta(days=random.randint(0, 30))
    positionen = []
    for _ in range(random.randint(1, 4)):
        produkt = random.choice(produkte)
        menge = random.randint(10, 100)
        einzelpreis = round(random.uniform(0.5, 2.5), 2)
        positionen.append({
            "artikelnummer": produkt["artikelnummer"],
            "produktname": produkt["name"],
            "menge": menge,
            "einzelpreis": einzelpreis,
            "gesamtpreis": round(menge * einzelpreis, 2)
        })
    bestellschein = {
        "bestellschein_nr": f"BS{1000+nr}",
        "kunde": kunde,
        "datum": datum,
        "positionen": positionen,
        "gesamtwert": round(sum(p["gesamtpreis"] for p in positionen), 2),
        "lieferadresse": f"Straße {random.randint(1,99)}, {random.randint(10000,99999)} Stadt"
    }
    return bestellschein

def main():
    anzahl = 10
    print(f"Generiere {anzahl} Bestellscheine in MongoDB...")
    for i in range(anzahl):
        bestellschein = generate_bestellschein(i)
        collection.insert_one(bestellschein)
    print("Bestellscheine erfolgreich generiert!")

if __name__ == "__main__":
    main()