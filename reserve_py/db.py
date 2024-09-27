import sqlite3
from pathlib import Path

DATABASE = Path('./database.db')

def create_reservation_table():
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations(
            teacher,
            date,
            period,
            room,
            subject,
            people,
            comment
        )
        """
    )
    
    conn.execute(
        """
        
        """
    )
    
    conn.commit()
    conn.close()
