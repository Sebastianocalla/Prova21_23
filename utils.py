# app/utils.py
import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path, sep=';')

def save_to_csv(df, file_path):
    df.to_csv(file_path, sep=';', index=False)
