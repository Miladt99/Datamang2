import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        user="postgres",
        password="password",
        dbname="supplychain"
    )
    print("Verbindung erfolgreich!")
    conn.close()
except Exception as e:
    import traceback
    print("Fehler:", str(e))
    traceback.print_exc()