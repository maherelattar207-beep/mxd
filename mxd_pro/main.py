import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from core.settings_manager import SettingsManager
from core.license_manager import LicenseManager
from ui.license_dialog import LicenseDialog
from ui.welcome_dialog import WelcomeDialog

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)

    settings_manager = SettingsManager()
    license_manager = LicenseManager(settings_manager)

    if not license_manager.is_activated():
        license_dialog = LicenseDialog(license_manager)
        if license_dialog.exec_() != LicenseDialog.Accepted:
            sys.exit(0)

        # After successful activation, ask for name if not already set
        if not settings_manager.get_setting("user_name"):
            user_name, ok = QInputDialog.getText(None, "Welcome!", "Please enter your name:")
            if ok and user_name:
                settings_manager.set_setting("user_name", user_name)
            else:
                settings_manager.set_setting("user_name", "User") # Default name

    user_name = settings_manager.get_setting("user_name", "User")

    # Show welcome dialog only on the very first successful activation
    if not settings_manager.get_setting("welcome_shown", False):
        welcome_dialog = WelcomeDialog(user_name)
        welcome_dialog.exec_()
        settings_manager.set_setting("welcome_shown", True)

    from ui.main_window import MainWindow
    main_window = MainWindow(settings_manager, license_manager)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()