import sys
import logging
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QInputDialog

# Import core modules
from core.hardware import HardwareDetector
from core.settings_engine import SettingsManager
from core.licensing import LicenseManager
from core.stability_monitor import StabilityMonitor
from core.performance_manager import PerformanceManager
# Import other managers as they are created

# Import UI modules
from ui.main_window import MainWindow
from ui.license_dialog import LicenseDialog

def setup_logging(settings_dir):
    """Configures the global logger."""
    log_dir = os.path.join(settings_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'mxd_pro.log')
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger()

def main():
    """Main application entry point for MXD Pro."""
    app = QApplication(sys.argv)

    # --- Setup Core Components ---
    settings = SettingsManager(settings_dir='mxd_pro/settings')
    logger = setup_logging('mxd_pro/settings')

    # --- Pre-Launch Stability Check ---
    stability_monitor = StabilityMonitor(logger, settings)
    if stability_monitor.check_for_instability_flag():
        # ... (rollback logic)
        pass
    stability_monitor.set_instability_flag() # Set flag for current run

    # --- Licensing and First Run Flow ---
    license_manager = LicenseManager(settings)
    if not license_manager.is_activated():
        dialog = LicenseDialog(license_manager)
        if dialog.exec_() != QDialog.Accepted:
            sys.exit(1) # Exit if activation is cancelled

        # --- First-Run User Name Prompt ---
        user_name, ok = QInputDialog.getText(None, "Welcome to MXD Pro!", "Please enter your name:")
        settings.set_setting("user.name", user_name if ok and user_name else "User")
        settings.set_setting("app.first_run_complete", True)

    # --- Initialize Managers ---
    hardware = HardwareDetector(logger)
    hardware_info = hardware.get_system_summary()
    perf_manager = PerformanceManager(logger)

    # --- First-Run Hardware Report ---
    if not settings.get_setting("app.hardware_report_shown", False):
        mode = perf_manager.determine_and_set_mode(hardware_info, settings)
        # ... (Show hardware report QMessageBox)
        settings.set_setting("app.hardware_report_shown", True)

    # --- Initialize Main Window and Run App ---
    # Pass all necessary managers to the MainWindow
    window = MainWindow(settings, license_manager, hardware, perf_manager, logger)
    window.show()

    exit_code = app.exec_()

    # Clean shutdown
    stability_monitor.clear_instability_flag()
    sys.exit(exit_code)

if __name__ == "__main__":
    # Global exception handler
    def exception_hook(exctype, value, traceback):
        logging.getLogger().critical("Unhandled exception caught:", exc_info=(exctype, value, traceback))
        QMessageBox.critical(None, "Critical Error", f"An unhandled error occurred: {value}")
        sys.exit(1)
    sys.excepthook = exception_hook

    # Need to import os for the logger setup
    import os
    main()