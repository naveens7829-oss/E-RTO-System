import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT,username TEXT,password TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS dl_applications(id INTEGER PRIMARY KEY,name TEXT,age INT,doc TEXT,status TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS admin(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

conn.execute("""
CREATE TABLE IF NOT EXISTS vehicles(
id INTEGER PRIMARY KEY,
owner TEXT,
vehicle_no TEXT,
model TEXT,
status TEXT
)
""")

conn.commit()
conn.close()