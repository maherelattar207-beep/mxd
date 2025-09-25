import logging
import os
from datetime import datetime

class MXDLogger:
    def __init__(self, filename="mxd_pro.log", console=True, level=logging.INFO):
        self.filename = filename
        self.console = console
        self.level = level
        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger("MXDProLogger")
        self.logger.setLevel(self.level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh = logging.FileHandler(self.filename, encoding="utf-8")
        fh.setLevel(self.level)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        if self.console:
            ch = logging.StreamHandler()
            ch.setLevel(self.level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def get_logs(self, num_lines=500):
        if not os.path.exists(self.filename):
            return "No log file found."
        with open(self.filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) > num_lines:
                return "".join(lines[-num_lines:])
            return "".join(lines)

    def clear_logs(self):
        open(self.filename, "w", encoding="utf-8").close()
        self.logger.info(f"Logs cleared at {datetime.now().isoformat()}")

    def get_logfile_path(self):
        return os.path.abspath(self.filename)