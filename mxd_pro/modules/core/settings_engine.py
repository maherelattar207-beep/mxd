import os
import json
from datetime import datetime

class SettingsManager:
    def __init__(self, logger, filename="mxdpro_user_settings.json"):
        self.logger = logger
        self.filename = filename
        self.settings = self._load_settings()
        self.backup_dir = "mxdpro_backups"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)

    def _load_settings(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except Exception as e:
                self._log(f"Failed to load user settings: {e}")
        return {"app": {}, "games": {}}

    def save_settings(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.settings, f, indent=2)
            self._log("User/app settings saved.")
        except Exception as e:
            self._log(f"Failed to save user settings: {e}")

    def get_app_setting(self, key, default=None):
        return self.settings.get("app", {}).get(key, default)

    def set_app_setting(self, key, value):
        self.settings.setdefault("app", {})[key] = value
        self.save_settings()

    def get_game_settings(self, game_name):
        return self.settings.get("games", {}).get(game_name, {})

    def set_game_settings(self, game_name, settings):
        self.settings.setdefault("games", {})[game_name] = settings
        self.save_settings()

    def backup_game_settings(self, game_name):
        backup_path = os.path.join(self.backup_dir, f"{game_name}_backup_{self._timestamp()}.json")
        settings = self.get_game_settings(game_name)
        try:
            with open(backup_path, "w") as f:
                json.dump(settings, f, indent=2)
            self._log(f"Backup created for {game_name} at {backup_path}")
            return backup_path
        except Exception as e:
            self._log(f"Failed to backup settings for {game_name}: {e}")
            return None

    def restore_last_backup(self, game_name):
        backups = self._list_backups(game_name)
        if not backups:
            self._log(f"No backups found for {game_name}")
            return False
        backups.sort(reverse=True)
        latest = backups[0]
        try:
            with open(latest, "r") as f:
                settings = json.load(f)
            self.set_game_settings(game_name, settings)
            self._log(f"Restored backup for {game_name} from {latest}")
            return True
        except Exception as e:
            self._log(f"Failed to restore backup for {game_name}: {e}")
            return False

    def _list_backups(self, game_name):
        files = []
        for f in os.listdir(self.backup_dir):
            if f.startswith(f"{game_name}_backup_") and f.endswith(".json"):
                files.append(os.path.join(self.backup_dir, f))
        return files

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def get_all_game_settings(self):
        return self.settings.get("games", {})

    def remove_game_settings(self, game_name):
        if "games" in self.settings and game_name in self.settings["games"]:
            del self.settings["games"][game_name]
            self.save_settings()

    def export_all_settings(self, export_path):
        try:
            with open(export_path, "w") as f:
                json.dump(self.settings, f, indent=2)
            self._log(f"Exported all settings to {export_path}")
            return True
        except Exception as e:
            self._log(f"Failed to export all settings: {e}")
            return False

    def import_all_settings(self, import_path):
        try:
            with open(import_path, "r") as f:
                data = json.load(f)
            self.settings = data
            self.save_settings()
            self._log(f"Imported all settings from {import_path}")
            return True
        except Exception as e:
            self._log(f"Failed to import settings: {e}")
            return False