import sqlite3
import pandas as pd

# Funzione per caricare i dati normalizzati dal database
def load_data():
    conn = sqlite3.connect('pesca.db')
    df_economia = pd.read_sql_query("SELECT * FROM Economia_Pesca", conn)
    df_occupazione = pd.read_sql_query("SELECT * FROM Occupazione_Pesca", conn)
    df_produttivita = pd.read_sql_query("SELECT * FROM Produttivita_Pesca", conn)
    conn.close()
    return df_economia, df_occupazione, df_produttivita

# Definizione delle aree geografiche
regioni_italia = {
    'Nord-ovest': ['Valle d\'Aosta', 'Piemonte', 'Liguria', 'Lombardia'],
    'Nord-est': ['Trentino-Alto Adige', 'Veneto', 'Friuli-Venezia Giulia', 'Emilia-Romagna'],
    'Centro': ['Toscana', 'Umbria', 'Marche', 'Lazio', 'Abruzzo'],
    'Sud': ['Molise', 'Campania', 'Puglia', 'Basilicata', 'Calabria'],
    'Isole': ['Sicilia', 'Sardegna']
}

# Funzione per calcolare la produttività totale per area e nazionale
def calculate_productivity(df):
    df['produttivita_migliaia'] = df['produttivita'] / 1000
    produttivita_areas = df.groupby(['anno', 'regione']).sum()['produttivita_migliaia'].reset_index()

    produttivita_totale_area = []
    produttivita_totale_nazionale = produttivita_areas.groupby('anno')['produttivita_migliaia'].sum().reset_index()
    produttivita_totale_nazionale['regione'] = 'Nazionale'
    produttivita_totale_nazionale = produttivita_totale_nazionale[['anno', 'regione', 'produttivita_migliaia']]
    
    for area, regioni in regioni_italia.items():
        area_data = produttivita_areas[produttivita_areas['regione'].isin(regioni)]
        area_productivity = area_data.groupby('anno')['produttivita_migliaia'].sum().reset_index()
        area_productivity['regione'] = area
        produttivita_totale_area.append(area_productivity)
    
    produttivita_totale_area = pd.concat(produttivita_totale_area)
    return pd.concat([produttivita_totale_area, produttivita_totale_nazionale])

# Funzione per calcolare la media percentuale valore aggiunto per area
def calculate_average_value_added(df):
    df['percentuale_valore_aggiunto'] = df['valore_aggiunto'] / df.groupby('anno')['valore_aggiunto'].transform('sum') * 100
    valore_aggiunto_areas = df.groupby(['anno', 'regione']).mean()['percentuale_valore_aggiunto'].reset_index()

    valore_aggiunto_totale = []
    
    for area, regioni in regioni_italia.items():
        area_data = valore_aggiunto_areas[valore_aggiunto_areas['regione'].isin(regioni)]
        area_value_added = area_data.groupby('anno')['percentuale_valore_aggiunto'].mean().reset_index()
        area_value_added['regione'] = area
        valore_aggiunto_totale.append(area_value_added)
    
    return pd.concat(valore_aggiunto_totale)

# Funzione per calcolare la variazione percentuale occupazione
def calculate_occupational_variation(df):
    df['occupazione_var_percentuale'] = df.groupby('regione')['occupazione'].pct_change() * 100
    occupazione_areas = df.groupby(['anno', 'regione']).mean()['occupazione_var_percentuale'].reset_index()

    occupazione_totale_area = []
    occupazione_totale_nazionale = occupazione_areas.groupby('anno')['occupazione_var_percentuale'].mean().reset_index()
    occupazione_totale_nazionale['regione'] = 'Nazionale'
    occupazione_totale_nazionale = occupazione_totale_nazionale[['anno', 'regione', 'occupazione_var_percentuale']]
    
    for area, regioni in regioni_italia.items():
        area_data = occupazione_areas[occupazione_areas['regione'].isin(regioni)]
        area_occupational_variation = area_data.groupby('anno')['occupazione_var_percentuale'].mean().reset_index()
        area_occupational_variation['regione'] = area
        occupazione_totale_area.append(area_occupational_variation)
    
    occupazione_totale_area = pd.concat(occupazione_totale_area)
    return pd.concat([occupazione_totale_area, occupazione_totale_nazionale])

# Funzione per salvare le serie calcolate nel database
def save_series_to_db(series_df, series_name):
    conn = sqlite3.connect('pesca.db')
    cursor = conn.cursor()
    
    for index, row in series_df.iterrows():
        cursor.execute('''
            INSERT INTO Serie_Calcolate (tipo, regione, anno, valore) 
            VALUES (?, ?, ?, ?)
        ''', (series_name, row['regione'], row['anno'], row.iloc[2]))
    
    conn.commit()
    conn.close()

# Funzione principale per il calcolo delle serie
def calculate_series():
    df_economia, df_occupazione, df_produttivita = load_data()

    # Calcolo della produttività totale
    produttivita_series = calculate_productivity(df_produttivita)
    save_series_to_db(produttivita_series, 'produttivita_totale')
    
    # Calcolo della media percentuale valore aggiunto
    valore_aggiunto_series = calculate_average_value_added(df_economia)
    save_series_to_db(valore_aggiunto_series, 'media_percentuale_valore_aggiunto')
    
    # Calcolo della variazione percentuale occupazione
    occupazione_series = calculate_occupational_variation(df_occupazione)
    save_series_to_db(occupazione_series, 'variazione_percentuale_occupazione')

if __name__ == "__main__":
    calculate_series()
    print("Series calculated and saved to database successfully.")
