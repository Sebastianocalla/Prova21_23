# app/create_database.py
from database import get_connection

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Economia_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT,
        anno INTEGER,
        valore_aggiunto REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Occupazione_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT,
        anno INTEGER,
        occupazione INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Produttivita_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT,
        anno INTEGER,
        produttivita REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Serie_Calcolate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        regione TEXT,
        anno INTEGER,
        valore REAL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully.")
