CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birthday TEXT NOT NULL,
    streak INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE role_champion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    champion_time INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    method INTEGER NOT NULL,
    channel_name TEXT NOT NULL,
    population INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);