from datetime import date, datetime
import sqlite3
import os

class Storage:
    def __init__(self):
        db_dir = os.path.join("cogs", "events", "db")
        filename = "alexandre.db"
        database = os.path.join(db_dir, filename)

        if not os.path.exists(database):
            raise FileNotFoundError

        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def add_log(self, user_id: int, method: str, channel_name: str, population: int):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO log (datetime, user_id, method, channel_name, population) VALUES (?, ?, ?, ?, ?);"
        with self.conn:
            self.cursor.execute(sql, (time, user_id, method, channel_name, population))

    def add_user(self, username: str, birthday: str):
        sql = "INSERT INTO user (name, birthday) VALUES (?, ?);"
        with self.conn:
            self.cursor.execute(sql, (username, birthday))

    def add_role(self, role_name: str):
        sql = "INSERT INTO role (name) VALUES (?);"
        with self.conn:
            self.cursor.execute(sql, (role_name,))

    def add_champion(self, user_id: int, role_id: int, time: int):
        sql = "INSERT INTO role_champion (user_id, role_id, champion_time) VALUES (?, ?, ?);"
        with self.conn:
            self.cursor.execute(sql, (user_id, role_id, time))
            
    def get_users(self):
        sql = "SELECT id, name, birthday, streak FROM user;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [
            {"id": r[0], "name": r[1], "birthday": r[2], "streak": r[3]}
            for r in rows
        ]

    def get_logs(self):
        sql = "SELECT id, datetime, user_id, method, channel_name, population FROM log;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [
            {"id": r[0], "datetime": r[1], "user_id": r[2], "method": r[3], "channel_name": r[4], "population": r[5]}
            for r in rows
        ]

    def yield_logs(self):
        sql = "SELECT log.id, log.datetime, log.user_id, user.name, log.method, log.channel_name, log.population FROM log JOIN user ON log.user_id = user.id;"
        self.cursor.execute(sql)
        for row in self.cursor.execute(sql):
            yield {
                "id": row[0],
                "datetime": row[1],
                "user_id": row[2],
                "username": row[3],
                "method": row[4],
                "channel_name": row[5],
                "population": row[6],
            }

    def get_roles(self):
        sql = "SELECT id, name FROM role;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [
            {"id": r[0], "name": r[1]}
            for r in rows
        ]

# Après le script setup create_db.py
if __name__ == "__main__":
    import csv
    
    storage = Storage()
    
    bday_dir = os.path.join("private")
    filename = "birthdays.csv"
    birthdays = os.path.join(bday_dir, filename)
    
    # ajout des users de base
    with open(birthdays, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            if i == 0:
                continue
            username, bday = line
            storage.add_user(username, bday)