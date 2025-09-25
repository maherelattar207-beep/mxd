import os
import json
import logging

class SettingsManager:
    """Manages loading, saving, and accessing application settings."""
    def __init__(self, settings_dir="mxd_pro/settings"):
        self.settings_dir = settings_dir
        self.settings_path = os.path.join(self.settings_dir, "user_preferences.json")
        os.makedirs(self.settings_dir, exist_ok=True)
        self.settings = self._load_settings()

    def _load_settings(self):
        """Loads settings from the JSON file."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Failed to load settings: {e}")
        return {} # Return empty dict if file doesn't exist or is corrupt

    def get_setting(self, key, default=None):
        """Gets a specific setting value."""
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """Sets a specific setting value and saves it."""
        self.settings[key] = value
        self._save_settings()

    def _save_settings(self):
        """Saves the current settings to the JSON file."""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            logging.error(f"Failed to save settings: {e}")