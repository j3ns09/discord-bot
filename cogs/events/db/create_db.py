import os
import sqlite3

create_user = """
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birthday TEXT NOT NULL,
    streak INTEGER NOT NULL DEFAULT 0
);
"""

create_role = """
CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
"""

create_role_champion = """
CREATE TABLE role_champion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    champion_time INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
"""

create_log = """
CREATE TABLE log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    method INTEGER NOT NULL,
    channel_name TEXT NOT NULL,
    population INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
"""

if __name__ == "__main__":
    db_dir = os.path.join("cogs", "events", "db")
    filename = "alexandre.db"
    database = os.path.join(db_dir, filename)

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(create_user)
    cursor.execute(create_role)
    cursor.execute(create_role_champion)
    cursor.execute(create_log)

    conn.commit()
    conn.close()
