import sqlite3
import pandas as pd

def load_data():
    """
    Carica i dati dal database SQLite in DataFrames.
    
    Returns:
    - df_economia (pd.DataFrame): Dati economici delle pesca.
    - df_occupazione (pd.DataFrame): Dati di occupazione delle pesca.
    - df_produttivita (pd.DataFrame): Dati di produttività delle pesca.
    """
    conn = sqlite3.connect('pesca.db')
    df_economia = pd.read_sql_query("SELECT regione, anno, valore_aggiunto FROM Economia_Pesca", conn)
    df_occupazione = pd.read_sql_query("SELECT regione, anno, occupazione FROM Occupazione_Pesca", conn)
    df_produttivita = pd.read_sql_query("SELECT regione, anno, produttivita FROM Produttivita_Pesca", conn)
    conn.close()

    return df_economia, df_occupazione, df_produttivita

def interpolate_data(df, value_column):
    """
    Interpola i dati in un DataFrame che ha le colonne 'regione' e 'anno' come variabili.
    
    Args:
    - df (pd.DataFrame): Il DataFrame contenente i dati con le colonne 'regione' e 'anno'.
    - value_column (str): Il nome della colonna sui cui dati interpolare.
    
    Returns:
    - pd.DataFrame: Il DataFrame con i dati interpolati.
    """
    # Assicurati che la colonna 'anno' sia di tipo int
    df['anno'] = df['anno'].astype(int)
    
    # Usa il metodo pivot per ottenere un formato adatto per l'interpolazione
    pivot_df = df.pivot(index='anno', columns='regione', values=value_column)

    # Interpola i dati
    pivot_df = pivot_df.interpolate(method='linear')

    # Resetta l'indice per ottenere di nuovo il formato DataFrame
    df_interpolated = pivot_df.reset_index()

    # Ripristina il formato a lungo con 'regione' e 'anno' come colonne
    df_interpolated = df_interpolated.melt(id_vars=['anno'], var_name='regione', value_name=value_column)

    # Assicuriamoci che il tipo di dato della colonna sia corretto
    df_interpolated[value_column] = df_interpolated[value_column].astype(float)
    
    return df_interpolated

def post_process_data():
    """
    Esegue il post-processing dei dati, comprese le interpolazioni e la stampa dei risultati.
    """
    df_economia, df_occupazione, df_produttivita = load_data()
    
    df_economia = interpolate_data(df_economia, 'valore_aggiunto')
    df_occupazione = interpolate_data(df_occupazione, 'occupazione')
    df_produttivita = interpolate_data(df_produttivita, 'produttivita')
    
    # Stampa i primi dati interpolati per verifica
    print("Dati interpolati per economia:")
    print(df_economia.head())
    
    print("\nDati interpolati per occupazione:")
    print(df_occupazione.head())
    
    print("\nDati interpolati per produttività:")
    print(df_produttivita.head())

if __name__ == "__main__":
    post_process_data()
