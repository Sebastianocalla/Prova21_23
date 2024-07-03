# app/post_process.py
import pandas as pd
from database import get_connection

def interpolate_data(df, value_column):
    df.set_index(['anno', 'regione'], inplace=True)
    df[value_column] = df.groupby(level=1)[value_column].apply(lambda group: group.interpolate(method='linear'))
    df.reset_index(inplace=True)
    return df

def save_to_csv(df, file_path):
    df.to_csv(file_path, sep=';', index=False)

def main():
    with get_connection() as conn:
        economia_df = pd.read_sql_query("SELECT * FROM Economia_Pesca", conn)
        occupazione_df = pd.read_sql_query("SELECT * FROM Occupazione_Pesca", conn)
        produttivita_df = pd.read_sql_query("SELECT * FROM Produttivita_Pesca", conn)
    
    economia_df = interpolate_data(economia_df, 'valore_aggiunto')
    occupazione_df = interpolate_data(occupazione_df, 'occupazione')
    produttivita_df = interpolate_data(produttivita_df, 'produttivita')
    
    save_to_csv(economia_df, 'data/Economia_Pesca_processed.csv')
    save_to_csv(occupazione_df, 'data/Occupazione_Pesca_processed.csv')
    save_to_csv(produttivita_df, 'data/Produttivita_Pesca_processed.csv')
    
    print("Data processing completed and files saved.")

if __name__ == "__main__":
    main()
