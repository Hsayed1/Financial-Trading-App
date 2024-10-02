# database.py
import sqlite3

DATABASE = 'portfolio.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# Create the portfolio table if it doesn't exist
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_name TEXT NOT NULL,
            purchase_price REAL NOT NULL,
            count INTEGER NOT NULL
        )
    ''')
    conn.commit()
