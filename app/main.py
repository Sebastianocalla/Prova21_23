# app/main.py
from fastapi import FastAPI
import pandas as pd
from database import get_connection

app = FastAPI()

def query_to_dataframe(query):
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)
    return df

@app.get("/economia/")
async def read_economia():
    df = query_to_dataframe("SELECT * FROM Economia_Pesca")
    return df.to_dict(orient="records")

@app.get("/occupazione/")
async def read_occupazione():
    df = query_to_dataframe("SELECT * FROM Occupazione_Pesca")
    return df.to_dict(orient="records")

@app.get("/produttivita/")
async def read_produttivita():
    df = query_to_dataframe("SELECT * FROM Produttivita_Pesca")
    return df.to_dict(orient="records")

@app.get("/serie_calcolate/")
async def read_serie_calcolate():
    df = query_to_dataframe("SELECT * FROM Serie_Calcolate")
    return df.to_dict(orient="records")

@app.post("/serie_calcolate/")
async def create_serie_calcolata(tipo: str, regione: str, anno: int, valore: float):
    query = """
    INSERT INTO Serie_Calcolate (tipo, regione, anno, valore)
    VALUES (?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (tipo, regione, anno, valore))
        conn.commit()
    return {"message": "Serie calcolata aggiunta con successo"}
