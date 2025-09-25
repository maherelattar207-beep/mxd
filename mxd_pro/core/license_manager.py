import logging

class LicenseManager:
    """Handles license activation and verification."""
    MASTER_KEY = "K!nG0FDr@g0nS"

    def __init__(self, settings_manager):
        self.settings = settings_manager

    def is_activated(self):
        """Checks if the application is activated."""
        return self.settings.get_setting("is_activated", False)

    def activate(self, key):
        """
        Activates the application with a license key.
        Returns True for successful activation, False otherwise.
        """
        if self._verify_key(key):
            self.settings.set_setting("is_activated", True)
            logging.info("Application activated successfully.")
            return True
        logging.warning(f"Activation failed with key: {key}")
        return False

    def _verify_key(self, key):
        """
        Verifies the license key.
        For now, it accepts the master key or any non-empty key (placeholder).
        """
        if key == self.MASTER_KEY:
            logging.info("Master key used for activation.")
            return True
        # Placeholder for real key verification logic
        return bool(key)

    def deactivate(self):
        """Deactivates the application."""
        self.settings.set_setting("is_activated", False)
        logging.info("Application deactivated.")