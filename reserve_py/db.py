import sqlite3

DATABASE = 'database.db'

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
    conn.close()
