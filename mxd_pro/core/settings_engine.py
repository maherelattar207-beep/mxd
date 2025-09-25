import os
import json
import logging

class SettingsManager:
    """Manages loading, saving, and accessing all application settings."""
    def __init__(self, settings_dir="mxd_pro/settings"):
        self.settings_dir = settings_dir
        self.settings_path = os.path.join(self.settings_dir, "user_preferences.json")
        os.makedirs(self.settings_dir, exist_ok=True)
        self.settings = self._load_settings()
        self.logger = logging.getLogger(__name__)

    def _load_settings(self):
        """Loads settings from the JSON file, returning an empty dict on failure."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Failed to load settings from {self.settings_path}: {e}")
        return {}

    def get_setting(self, key, default=None):
        """
        Gets a specific setting value by key.
        Uses dot notation for nested access, e.g., 'app.theme'.
        """
        keys = key.split('.')
        val = self.settings
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    def set_setting(self, key, value):
        """
        Sets a specific setting value by key and saves it.
        Uses dot notation for nested access.
        """
        keys = key.split('.')
        d = self.settings
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        self._save_settings()

    def _save_settings(self):
        """Saves the current settings dictionary to the JSON file."""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            self.logger.error(f"Failed to save settings to {self.settings_path}: {e}")