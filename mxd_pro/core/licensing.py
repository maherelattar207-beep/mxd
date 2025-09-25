import logging
from .settings_engine import SettingsManager

class LicenseManager:
    """Handles license activation and verification."""
    MASTER_KEY = "K!nG0FDr@g0nS"

    def __init__(self, settings_manager: SettingsManager):
        self.settings = settings_manager
        self.logger = logging.getLogger(__name__)

    def is_activated(self) -> bool:
        """Checks if the application is activated by reading from settings."""
        return self.settings.get_setting("license.is_activated", False)

    def activate(self, key: str) -> bool:
        """
        Activates the application with a license key.
        Returns True for successful activation, False otherwise.
        """
        if self._verify_key(key):
            self.settings.set_setting("license.is_activated", True)
            self.settings.set_setting("license.key", key if key != self.MASTER_KEY else "MASTER")
            self.logger.info("Application activated successfully.")
            return True
        self.logger.warning(f"Activation failed with key: {key}")
        return False

    def _verify_key(self, key: str) -> bool:
        """
        Verifies the license key. For this offline version, it accepts the
        master key or any non-empty key as a placeholder for real validation.
        """
        if not key:
            return False
        if key == self.MASTER_KEY:
            self.logger.info("Master key used for activation.")
            return True

        # Placeholder for a real, offline-capable key verification algorithm.
        # For now, we'll accept any key that looks like a key.
        if len(key) > 10 and "-" in key:
            return True

        return False

    def deactivate(self):
        """Deactivates the application by updating the settings."""
        self.settings.set_setting("license.is_activated", False)
        self.logger.info("Application license deactivated.")