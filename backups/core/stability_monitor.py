import time
import random
from PyQt5.QtCore import QThread, pyqtSignal

class StabilityMonitor(QThread):
    """
    A background thread to monitor for simulated system instability after
    new game settings are applied.
    """
    instability_detected = pyqtSignal(str) # Emits the game name

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.monitoring = False
        self.game_name = None

    def start_monitoring(self, game_name: str):
        """Starts the monitoring thread for a specific game."""
        if self.isRunning():
            self.stop_monitoring()

        self.game_name = game_name
        self.monitoring = True
        self.logger.info(f"Stability monitor started for {self.game_name}.")
        self.start()

    def stop_monitoring(self):
        """Stops the monitoring thread."""
        self.monitoring = False
        if self.isRunning():
            self.logger.info(f"Stability monitor stopped for {self.game_name}.")
            self.wait() # Wait for the thread to finish cleanly

    def run(self):
        """
        The main loop for the monitoring thread.
        Simulates checking for instability.
        """
        # Give the system a moment to "settle" after applying settings
        time.sleep(10)

        check_interval_seconds = 5
        monitoring_duration_seconds = 60 # Monitor for 1 minute

        for i in range(monitoring_duration_seconds // check_interval_seconds):
            if not self.monitoring:
                return

            self.logger.info(f"Stability check {i+1} for {self.game_name}...")

            # Simulate a 5% chance of detecting instability on each check
            if random.randint(1, 100) <= 5:
                self.logger.warning(f"Simulated instability detected for {self.game_name}!")
                self.instability_detected.emit(self.game_name)
                self.monitoring = False
                return

            time.sleep(check_interval_seconds)

        self.logger.info(f"Monitoring period for {self.game_name} ended. System appears stable.")
        self.monitoring = False
