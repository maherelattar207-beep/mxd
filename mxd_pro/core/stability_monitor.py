import logging
from .settings_engine import SettingsManager

class StabilityMonitor:
    """
    Monitors for system instability flags and handles settings rollbacks.
    This is a simplified, non-threaded version for the initial merge.
    """
    def __init__(self, logger: logging.Logger, settings_manager: SettingsManager):
        self.logger = logger
        self.settings = settings_manager
        self.instability_flag_key = "app.had_crash_on_last_run"

    def check_for_instability_flag(self) -> bool:
        """Checks if the instability flag was set from a previous run."""
        return self.settings.get_setting(self.instability_flag_key, False)

    def set_instability_flag(self):
        """Sets a flag indicating the app is running and might crash."""
        self.logger.info("Setting instability flag (app is running).")
        self.settings.set_setting(self.instability_flag_key, True)

    def clear_instability_flag(self):
        """Clears the instability flag on a clean shutdown."""
        self.logger.info("Clearing instability flag (clean shutdown).")
        self.settings.set_setting(self.instability_flag_key, False)

    def backup_settings(self, section: str = "games"):
        """Creates a backup of a specific section of the settings."""
        self.logger.info(f"Backing up '{section}' settings before applying changes.")
        current_settings = self.settings.get_setting(section, {})
        self.settings.set_setting(f"backups.{section}", current_settings)

    def rollback_settings(self, section: str = "games") -> bool:
        """Rolls back settings for a specific section from the backup."""
        self.logger.warning(f"Rolling back '{section}' settings due to instability.")
        backup_settings = self.settings.get_setting(f"backups.{section}")
        if backup_settings is not None:
            self.settings.set_setting(section, backup_settings)
            self.logger.info(f"Successfully rolled back '{section}' settings.")
            return True
        else:
            self.logger.error(f"No backup found for section '{section}'. Cannot roll back.")
            return False