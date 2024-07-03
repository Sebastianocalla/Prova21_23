import pandas as pd
import sqlite3
import os

# Percorsi dei file CSV locali
csv_importanza_economica = "C:/Users/sebas/OneDrive/Desktop/Prova21_23/Importanza-economica-del-settore-della-pesca-per-regione (1).csv"
csv_occupazione = "C:/Users/sebas/OneDrive/Desktop/Prova21_23/Andamento-occupazione-del-settore-della-pesca-per-regione.csv"
csv_produttivita = "C:/Users/sebas/OneDrive/Desktop/Prova21_23/Produttivita-del-settore-della-pesca-per-regione.csv"

# Funzione per caricare i dati dai file CSV locali
def load_csv(file_path, delimiter=';'):
    if not os.path.isfile(file_path):
        print(f"File non trovato: {file_path}")
        return pd.DataFrame()  # Ritorna un DataFrame vuoto se il file non esiste
    
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        df.columns = df.columns.str.strip()  # Rimuove gli spazi dai nomi delle colonne
        print(f"Colonne nel file {file_path}: {df.columns.tolist()}")
        print(df.head())  # Mostra le prime righe del DataFrame per ispezionare i dati
        return df
    except pd.errors.ParserError as e:
        print(f"Errore di parsing per il file {file_path}: {e}")
        return pd.DataFrame()  # Ritorna un DataFrame vuoto in caso di errore
    except Exception as e:
        print(f"Errore imprevisto per il file {file_path}: {e}")
        return pd.DataFrame()  # Ritorna un DataFrame vuoto per qualsiasi altro errore

# Funzione per importare i dati nel database
def import_data():
    conn = sqlite3.connect('pesca.db')
    cursor = conn.cursor()

    # Crea la tabella Economia_Pesca se non esiste
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Economia_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT NOT NULL,
        anno INTEGER NOT NULL,
        valore_aggiunto REAL NOT NULL
    );
    ''')

    # Importanza economica
    df_importanza = load_csv(csv_importanza_economica, delimiter=';')
    if not df_importanza.empty:
        if 'Regione' not in df_importanza.columns or 'Anno' not in df_importanza.columns or 'Percentuale valore aggiunto pesca-piscicoltura-servizi' not in df_importanza.columns:
            print(f"Colonne attese nel file Importanza economica: ['Regione', 'Anno', 'Percentuale valore aggiunto pesca-piscicoltura-servizi']")
        for index, row in df_importanza.iterrows():
            cursor.execute('''
                INSERT INTO Economia_Pesca (regione, anno, valore_aggiunto) 
                VALUES (?, ?, ?)
            ''', (row['Regione'], row['Anno'], row['Percentuale valore aggiunto pesca-piscicoltura-servizi']))

    # Crea la tabella Occupazione_Pesca se non esiste
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Occupazione_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT NOT NULL,
        anno INTEGER NOT NULL,
        occupazione INTEGER NOT NULL
    );
    ''')

    # Occupazione
    df_occupazione = load_csv(csv_occupazione, delimiter=';')
    if not df_occupazione.empty:
        if 'Regione' not in df_occupazione.columns or 'Anno' not in df_occupazione.columns or 'Occupazione' not in df_occupazione.columns:
            print(f"Colonne attese nel file Occupazione: ['Regione', 'Anno', 'Occupazione']")
        for index, row in df_occupazione.iterrows():
            cursor.execute('''
                INSERT INTO Occupazione_Pesca (regione, anno, occupazione) 
                VALUES (?, ?, ?)
            ''', (row['Regione'], row['Anno'], row['Occupazione']))

    # Crea la tabella Produttivita_Pesca se non esiste
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Produttivita_Pesca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        regione TEXT NOT NULL,
        anno INTEGER NOT NULL,
        produttivita REAL NOT NULL
    );
    ''')

    # Produttività
    df_produttivita = load_csv(csv_produttivita, delimiter=';')
    if not df_produttivita.empty:
        if 'Regione' not in df_produttivita.columns or 'Anno' not in df_produttivita.columns or 'Produttività' not in df_produttivita.columns:
            print(f"Colonne attese nel file Produttività: ['Regione', 'Anno', 'Produttività']")
        for index, row in df_produttivita.iterrows():
            cursor.execute('''
                INSERT INTO Produttivita_Pesca (regione, anno, produttivita) 
                VALUES (?, ?, ?)
            ''', (row['Regione'], row['Anno'], row['Produttività']))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_data()
    print("Data imported successfully.")