# app/import_data.py
import pandas as pd
from database import get_connection
from create_database import create_database

def import_data():
    economia_df = pd.read_csv('data/Economia_Pesca.csv', sep=';')
    occupazione_df = pd.read_csv('data/Occupazione_Pesca.csv', sep=';')
    produttivita_df = pd.read_csv('data/Produttivita_Pesca.csv', sep=';')

    create_database()

    with get_connection() as conn:
        economia_df.to_sql('Economia_Pesca', conn, if_exists='append', index=False)
        occupazione_df.to_sql('Occupazione_Pesca', conn, if_exists='append', index=False)
        produttivita_df.to_sql('Produttivita_Pesca', conn, if_exists='append', index=False)
    
    print("Data imported successfully.")

if __name__ == "__main__":
    import_data()
