import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from core.hardware import HardwareDetector
from core.optimizer import GamingOptimizer, AIPerformanceOptimizer
from core.utils import initialize_mxd_pro
from core.licensing import LicenseManager
from core.performance_manager import PerformanceManager
from core.security_manager import SecurityManager
from core.localization_manager import LocalizationManager
from core.response_manager import ResponseTimeManager
from ui.main_window import MainWindow
from ui.license_dialog import LicenseDialog

def main():
    app = QApplication(sys.argv)
    logger, settings, _, _ = initialize_mxd_pro()

    # Load Theme
    try:
        with open("backups/ui/theme.qss", "r") as f:
            app.setStyleSheet(f.read())
        logger.info("UI theme loaded successfully.")
    except FileNotFoundError:
        logger.error("Could not find theme.qss. Using default system style.")

    # --- New, Correct Licensing Flow ---
    license_manager = LicenseManager(logger)
    if not license_manager.verify_license():
        logger.warning("License not valid or not found. Showing activation dialog.")
        dialog = LicenseDialog(license_manager, logger)
        if dialog.exec_() != QDialog.Accepted:
            logger.critical("License activation failed or was cancelled by user. Exiting.")
            sys.exit(1)

    logger.info("License check passed. Starting main application.")

    # --- Initialize all managers and run the app ---
    hardware = HardwareDetector(logger)
    hardware_info = hardware.get_system_summary()
    perf_manager = PerformanceManager(logger)

    # Determine performance mode and show first-run report if applicable
    is_first_run = settings.get("first_run", True)
    detected_mode = perf_manager.determine_and_set_mode(hardware_info, settings)
    if is_first_run:
        cpu = hardware_info.get("cpu"); gpu = hardware_info.get("gpus")[0] if hardware_info.get("gpus") else None; ram = hardware_info.get("memory")
        report = f"<b>Welcome to MXD Pro!</b><br><br>We've analyzed your system and set an initial performance profile.<br><br><b>Detected Hardware:</b><br>- CPU: {cpu.name if cpu else 'N/A'}<br>- GPU: {gpu.name if gpu else 'N/A'}<br>- RAM: {ram.total_mb / 1024:.1f} GB<br><br><b>Performance Profile Set:</b> {detected_mode.value}"
        QMessageBox.information(None, "First-Time Setup", report)

    gaming_optimizer = GamingOptimizer(logger, settings)
    ai_optimizer = AIPerformanceOptimizer(logger, settings)
    security_manager = SecurityManager(logger, settings)
    loc_manager = LocalizationManager(logger, settings)
    response_manager = ResponseTimeManager(logger, settings)

    window = MainWindow(
        hardware=hardware, games=gaming_optimizer, settings=settings,
        perf_manager=perf_manager, ai_optimizer=ai_optimizer,
        security_manager=security_manager, loc_manager=loc_manager,
        response_manager=response_manager, logger=logger
    )

    window.show()

    try:
        exit_code = app.exec_()
    finally:
        logger.shutdown()

    sys.exit(exit_code)

if __name__ == "__main__":
    main()