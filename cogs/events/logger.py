from datetime import date, datetime
import time


class Logger:
    def __init__(self, filename):
        self.creation_time = datetime.now()
        self.filename = filename

        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(
                f"=== Log created {self.creation_time.strftime('%Y-%m-%d %H:%M:%S')} ===\n"
            )

    def write(self, line: str) -> None:
        """Write a line to the log, resetting file if 7 days have passed."""
        # Check for reset
        if self._is_week_old():
            self.reset()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {line}\n")

    def reset(self) -> None:
        """Reset the log file and update creation time."""
        # Optionally back up the old log
        if os.path.exists(self.filename):
            backup_name = self.filename.replace(
                ".log", f"_{self.creation_time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
            )
            os.rename(self.filename, backup_name)

        # Create new file
        self.creation_time = datetime.now()
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(
                f"=== Log reset on {self.creation_time.strftime('%Y-%m-%d %H:%M:%S')} ===\n"
            )
