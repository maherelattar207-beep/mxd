import time
from PyQt5.QtCore import QThread, pyqtSignal
import random

class RealTimeMonitor(QThread):
    """A background thread that simulates real-time threat detection."""
    threat_detected = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.threat_scenarios = [
            {"name": "Trojan.Generic.12345", "type": "Trojan", "risk_score": 85},
            {"name": "Adware.InstallCore.789", "type": "Adware", "risk_score": 40},
            {"name": "Ransom.WannaCry.PoC", "type": "Ransomware", "risk_score": 99},
            {"name": "Miner.CoinHive.X", "type": "Cryptominer", "risk_score": 65},
        ]

    def run(self):
        """The main loop for the monitoring thread."""
        while self.running:
            time.sleep(random.randint(10, 30)) # Wait for a random interval
            if self.running and random.choice([True, False]):
                threat = random.choice(self.threat_scenarios)
                self.threat_detected.emit(threat)

    def stop(self):
        """Stops the monitoring thread."""
        self.running = False