from pymongo import MongoClient

# Verbindung ohne Authentifizierung
client = MongoClient('mongodb://localhost:27017/')

# Datenbank auswählen
db = client['testdb']

# Collection erstellen und testen
collection = db['test']
collection.insert_one({"test": "Hello MongoDB!"})

print("MongoDB funktioniert!")