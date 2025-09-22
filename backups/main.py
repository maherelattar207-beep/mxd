import sys
from PyQt5.QtWidgets import QApplication
from core.hardware import HardwareDetector
from core.optimizer import GamingOptimizer, AIPerformanceOptimizer
from core.utils import initialize_mxd_pro
from core.licensing import LicenseManager
from core.performance_manager import PerformanceManager
from core.security_manager import SecurityManager
from core.localization_manager import LocalizationManager
from core.response_manager import ResponseTimeManager
from ui.main_window import MainWindow
from PyQt5.QtWidgets import QMessageBox

def main():
    app = QApplication(sys.argv)

    # Initialize core components
    logger, settings, safe_mode, profiles_db = initialize_mxd_pro()

    # Load and apply the theme
    try:
        with open("backups/ui/theme.qss", "r") as f:
            app.setStyleSheet(f.read())
        logger.info("UI theme loaded successfully.")
    except FileNotFoundError:
        logger.error("Could not find theme.qss. The application will use the default system style.")

    # Ensure a valid license exists, or create one
    license_manager = LicenseManager(logger)
    license_manager.ensure_license_is_valid()

    logger.info("License check passed. Starting main application.")

    # Initialize hardware detection
    hardware = HardwareDetector(logger)
    hardware_info = hardware.get_system_summary()

    # Determine and set performance mode
    perf_manager = PerformanceManager(logger)
    is_first_run = settings.get("first_run", True)
    detected_mode = perf_manager.determine_and_set_mode(hardware_info, settings)

    # On first run, show a summary report
    if is_first_run:
        cpu = hardware_info.get("cpu")
        gpu = hardware_info.get("gpus")[0] if hardware_info.get("gpus") else None
        ram = hardware_info.get("memory")
        report = f"""
        <b>Welcome to MXD Pro!</b><br><br>
        We've analyzed your system and set an initial performance profile.<br><br>
        <b>Detected Hardware:</b><br>
        - <b>CPU:</b> {cpu.name if cpu else 'N/A'}<br>
        - <b>GPU:</b> {gpu.name if gpu else 'N/A'}<br>
        - <b>RAM:</b> {ram.total_mb / 1024:.1f} GB<br><br>
        <b>Performance Profile Set:</b> {detected_mode.value}<br><br>
        You can change this at any time in the Settings tab.
        """
        QMessageBox.information(None, "First-Time Setup", report)

    # Initialize all manager modules
    gaming_optimizer = GamingOptimizer(logger, settings)
    ai_optimizer = AIPerformanceOptimizer(logger, settings)
    security_manager = SecurityManager(logger, settings)
    loc_manager = LocalizationManager(logger, settings)
    response_manager = ResponseTimeManager(logger, settings)

    # The main window will need all the managers to pass to its panels.
    window = MainWindow(
        hardware=hardware,
        games=gaming_optimizer,
        settings=settings,
        perf_manager=perf_manager,
        ai_optimizer=ai_optimizer,
        security_manager=security_manager,
        loc_manager=loc_manager,
        response_manager=response_manager,
        logger=logger
    )

    window.show()

    try:
        exit_code = app.exec_()
    finally:
        # Ensure logs are saved on exit
        logger.shutdown()

    sys.exit(exit_code)

if __name__ == "__main__":
    main()