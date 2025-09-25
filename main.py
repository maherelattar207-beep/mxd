import sys
from PyQt5.QtWidgets import QApplication
from core.hardware import HardwareInfo
from core.game_profiles import GameProfileManager
from core.settings_engine import SettingsManager
from core.logger import MXDLogger
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    logger = MXDLogger()
    hardware = HardwareInfo(logger)
    games = GameProfileManager(logger, hardware)
    settings = SettingsManager(logger)
    window = MainWindow(hardware, games, settings, logger)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()