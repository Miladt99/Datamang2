import sqlite3
from generate_data import insert_data


def test_insert_data(temp_db):
    insert_data()
    conn = sqlite3.connect(temp_db)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM ernte')
    count = cur.fetchone()[0]
    conn.close()
    assert count == 10