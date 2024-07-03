# app/database.py
import sqlite3

DATABASE_URL = 'data/pesca.db'

def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    return conn
