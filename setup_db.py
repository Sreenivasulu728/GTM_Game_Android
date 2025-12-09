import sqlite3

conn = sqlite3.connect("movies.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer TEXT,
    characters TEXT,
    hints TEXT,
    alternatives TEXT,
    level INTEGER,
    time INTEGER
)
""")

conn.commit()
conn.close()

print("Database ready!")
