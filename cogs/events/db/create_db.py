import os
import sqlite3


if __name__ == "__main__":
    db_dir = os.path.join("cogs", "events", "db")
    db_name = "alexandre.db"
    script_name = "create_db.sql"

    database = os.path.join(db_dir, db_name)
    script = os.path.join(db_dir, script_name)
    

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    with open(script, "r") as f:
        schema = f.read()

    conn.executescript(schema)
    conn.close()
