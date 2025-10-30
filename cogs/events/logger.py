import os
from datetime import datetime


class Logger:
    def __init__(self):
        self.creation_time: datetime = datetime.now()
        self.time_format: str = "%Y-%m-%d %H:%M:%S"

        logs_dir = os.path.join("cogs", "events", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        filename = f"trolleur_{self.creation_time.strftime('%Y-%m-%d')}.log"

        self.filename: str = os.path.join(logs_dir, filename)

        with open(self.filename, "w", encoding="utf-8") as f:
            _ = f.write(
                f"=== Log créé au {self.creation_time.strftime(self.time_format)} ===\n\n"
            )

    def write_logs(self, log_data: dict):
        with open(self.filename, "a", encoding="utf-8") as f:
            _ = f.write(f'{log_data["datetime"]} - {log_data["username"]} a {log_data["method"]} le salon vocal {log_data["channel_name"]} ({log_data["population"]} personne(s) présentes)\n')
# {
#     "id": row[0],
#     "datetime": row[1],
#     "user_id": row[2],
#     "username": row[3],
#     "method": row[4],
#     "channel_name": row[5],
#     "population": row[6],
# }
    def clean(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)


# For test purposes
if __name__ == "__main__":
    from storage import Storage
    import csv
    
    storage = Storage()    
    logger = Logger()
    for log in storage.yield_logs():
        logger.write_logs(log)