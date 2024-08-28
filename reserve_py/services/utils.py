import json
import sqlite3
from pathlib import Path

DATABASE = Path('./database.db')

def dict_factory(cursor, row):
    di = {}
    for idx, col in enumerate(cursor.description):
        di[col[0]] = row[idx]
    return di

def load_json(filename):
    with open(Path(f'./json/{filename}.json'), mode='r') as f:
        return json.load(f)

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    return conn

def close_connection(conn):
    if conn:
        conn.close()
