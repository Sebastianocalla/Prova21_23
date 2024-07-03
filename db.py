# in questo file ci sarà lo script per creare il database
import sqlite3


def create_database():
    conn = sqlite3.connect('pesca.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Economia_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT,
        anno INTEGER,
        valore_aggiunto INTEGER
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
        produttivita INTEGER
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