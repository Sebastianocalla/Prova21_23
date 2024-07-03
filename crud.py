# app/crud.py
import pandas as pd
from .database import get_connection

def load_data():
    with get_connection() as conn:
        economia_df = pd.read_sql_query("SELECT * FROM Economia_Pesca", conn)
        occupazione_df = pd.read_sql_query("SELECT * FROM Occupazione_Pesca", conn)
        produttivita_df = pd.read_sql_query("SELECT * FROM Produttivita_Pesca", conn)
    return economia_df, occupazione_df, produttivita_df

def get_economia_data():
    economia_df, _, _ = load_data()
    return economia_df.to_dict(orient='records')

def get_occupazione_data():
    _, occupazione_df, _ = load_data()
    return occupazione_df.to_dict(orient='records')

def get_produttivita_data():
    _, _, produttivita_df = load_data()
    return produttivita_df.to_dict(orient='records')
