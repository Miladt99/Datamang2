import psycopg2


def test_postgres_connection(postgres_conn):
    cur = postgres_conn.cursor()
    cur.execute('SELECT 1')
    assert cur.fetchone()[0] == 1
    cur.close()


def test_mongo_connection(mongo_client):
    db = mongo_client.testdb
    collection = db.test
    result = collection.insert_one({'foo': 'bar'})
    fetched = collection.find_one({'_id': result.inserted_id})
    assert fetched['foo'] == 'bar'