import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Core Components
from core.hardware import HardwareInfo
from core.game_profiles import GameProfileManager
from core.settings_engine import SettingsManager
from core.logger import MXDLogger
from core.licensing import LicensingManager
from core.stability_monitor import StabilityMonitor
from core.performance_manager import PerformanceManager
from core.ai_optimizer import AIOptimizer
from core.response_manager import ResponseManager

# UI Components
from ui.main_window import MainWindow
from ui.license_dialog import LicenseDialog

def run_pre_launch_checks(logger, hardware, settings):
    """Run critical pre-launch checks."""
    logger.info("MXD Pro Engine Initializing...")

    # Check for stability issues from last run
    monitor = StabilityMonitor(logger, settings)
    if monitor.check_for_instability_flag():
        logger.warning("Instability detected from previous session.")
        if monitor.rollback_settings():
            logger.info("Settings rollback successful.")
            QMessageBox.warning(None, "Stability Warning", "An instability was detected from the last session. Settings have been rolled back to a safe state.")
        else:
            logger.error("Settings rollback failed.")
            QMessageBox.critical(None, "Stability Error", "Failed to roll back settings. Please report this issue.")

    logger.info("Detecting Hardware...")
    hardware.get_system_summary() # Pre-cache hardware info
    logger.info("Hardware detection complete.")

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Initialize core components
    logger = MXDLogger()
    settings = SettingsManager(logger)
    hardware = HardwareInfo(logger)
    licensing = LicensingManager(settings, hardware, logger)

    # Pre-launch checks
    run_pre_launch_checks(logger, hardware, settings)

    # --- License Check ---
    logger.info("Verifying License...")

    if not licensing.is_license_valid():
        logger.warning("No valid license found. Displaying activation dialog.")
        dialog = LicenseDialog(licensing)
        if dialog.exec_() != LicenseDialog.Accepted:
            logger.error("License activation failed or was cancelled by user. Exiting.")
            QMessageBox.critical(None, "Activation Required", "A valid license is required to use MXD Pro.")
            sys.exit(1)
        logger.info("License activated successfully.")
    else:
        logger.info("Existing license verified successfully.")

    # --- Main Application Setup ---
    logger.info("Loading Components...")

    # Initialize remaining components that depend on a valid license
    games = GameProfileManager(logger, hardware)
    perf_manager = PerformanceManager(settings, hardware)
    response_manager = ResponseManager(settings, logger)
    ai_optimizer = AIOptimizer(logger, hardware)

    # --- Launch Main Window ---
    logger.info("Launching Main Interface...")

    main_window = MainWindow(hardware, games, settings, logger, perf_manager, response_manager, ai_optimizer)
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    # Setup exception hook
    def exception_hook(exctype, value, traceback):
        # Ensure logger is initialized, though it should be
        # For this hook, we might need a fallback logger if MXDLogger fails
        try:
            log = logging.getLogger("MXDLogger")
            log.critical("Unhandled exception caught:", exc_info=(exctype, value, traceback))
        except Exception:
            # Fallback to standard logging if MXDLogger has issues
            logging.basicConfig(level=logging.CRITICAL)
            logging.critical("Unhandled exception caught in hook:", exc_info=(exctype, value, traceback))

        sys.__excepthook__(exctype, value, traceback)
        QMessageBox.critical(None, "Unhandled Exception", f"A critical error occurred: {value}. Please check the logs for details.")
    sys.excepthook = exception_hook

    main()