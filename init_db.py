
import sqlite3

conn = sqlite3.connect('college.db')
with open('setup.sql', 'r') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()

print("Database initialized.")
