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

    def write_entry(self, msg: str):
        now = datetime.now()

        with open(self.filename, "a", encoding="utf-8") as f:
            _ = f.write(f"{now.strftime(self.time_format)} - {msg}\n")

    def clean(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)


# For test purposes
if __name__ == "__main__":
    logger = Logger()
    logger.write_entry("Hello this is a test")
