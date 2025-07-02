from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# Verbindung zu MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['supplychain']
collection = db['bestellscheine']

# Beispiel-Stammdaten
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

    # 📅 5 % der Daten mit falschem Datum (in der Zukunft)
    if random.random() < 0.05:
        datum = datetime.now() + timedelta(days=random.randint(1, 30))
    else:
        datum = datetime.now() - timedelta(days=random.randint(0, 30))

    positionen = []
    anzahl_positionen = random.randint(1, 4)
    for i in range(anzahl_positionen):
        # 📊 Szenario: Schmidt AG bestellt bevorzugt Tropenmix
        if kunde == "Schmidt AG":
            produkt = {"name": "Tropenmix", "artikelnummer": "T2001"}
        elif produkt := random.choice(produkte):

            # 📊 Szenario: Sommeraktion für Exotenbox (letzte 7 Tage = mehr davon)
            if (datetime.now() - datum).days < 7 and random.random() < 0.5:
                produkt = {"name": "Exotenbox", "artikelnummer": "E3001"}

        menge = random.randint(10, 100)

        # 💥 Qualitätsproblem: 3 % haben keine Menge
        if random.random() < 0.03:
            menge = None

        # 💥 Qualitätsproblem: 3 % haben extrem hohe Menge
        if random.random() < 0.03:
            menge = random.randint(1000, 10000)

        # 💥 Qualitätsproblem: 2 % haben negativen Preis
        if random.random() < 0.02:
            einzelpreis = round(random.uniform(-5.0, -0.1), 2)
        else:
            einzelpreis = round(random.uniform(0.5, 2.5), 2)

        # 💥 Doppelte Artikelnummern in Positionen (5 %)
        if i > 0 and random.random() < 0.05:
            produkt = positionen[0]["produktname"]

        if menge is None:
            gesamt = None
        else:
            gesamt = round(menge * einzelpreis, 2)

        positionen.append({
            "artikelnummer": produkt["artikelnummer"],
            "produktname": produkt["name"],
            "menge": menge,
            "einzelpreis": einzelpreis,
            "gesamtpreis": gesamt
        })

    bestellschein = {
        "bestellschein_nr": f"BS{1000+nr}",
        "kunde": kunde,
        "datum": datum,
        "positionen": positionen,
        "gesamtwert": round(sum(p["gesamtpreis"] or 0 for p in positionen), 2),
        "lieferadresse": f"Straße {random.randint(1,99)}, {random.randint(10000,99999)} Stadt"
    }
    return bestellschein

def main():
    anzahl = 1000
    print(f"Generiere {anzahl} Bestellscheine in MongoDB...")
    for i in range(anzahl):
        bestellschein = generate_bestellschein(i)
        collection.insert_one(bestellschein)
    print("Bestellscheine erfolgreich generiert!")

if __name__ == "__main__":
    main()
