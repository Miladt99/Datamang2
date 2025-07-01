from create_schema import create_tables
from generate_data import insert_data, insert_qc_data, insert_hafen_data, insert_dc_data, insert_pos_data, insert_transportauftraege
from mongo_insert import insert_bestellscheine

# def main():
#     create_tables()
#     insert_data()
#     insert_qc_data()
#     insert_hafen_data()
#     insert_dc_data()
#     insert_pos_data()
#     insert_transportauftraege()
#     insert_bestellscheine()  # 👈 MongoDB hinzufügen
#     print("✅ Komplettlauf abgeschlossen.")



def main():
    create_tables()
    insert_data()
    insert_qc_data()
    insert_hafen_data()
    insert_dc_data()
    insert_pos_data()
    insert_transportauftraege()
    insert_bestellscheine()
    print("✅ Komplettlauf abgeschlossen.")

if __name__ == "__main__":
    main()