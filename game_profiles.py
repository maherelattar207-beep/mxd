import os
import json

class GameProfile:
    def __init__(self, name, exe_names, config_paths, supported_resolutions, supports_6k, settings_schema):
        self.name = name
        self.exe_names = exe_names
        self.config_paths = config_paths
        self.supported_resolutions = supported_resolutions
        self.supports_6k = supports_6k
        self.settings_schema = settings_schema

    def as_dict(self):
        return {
            "name": self.name,
            "exe_names": self.exe_names,
            "config_paths": self.config_paths,
            "supported_resolutions": self.supported_resolutions,
            "supports_6k": self.supports_6k,
            "settings_schema": self.settings_schema
        }

class GameProfileManager:
    def __init__(self, logger, hardware):
        self.logger = logger
        self.hardware = hardware
        self.profiles = self._load_profiles()
        self.installed_games = self._detect_installed_games()

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)

    def _load_profiles(self):
        schema = {
            "resolution": {"type": "string", "options": ["1080p", "2K", "4K", "5K", "6K"]},
            "fps": {"type": "int", "min": 30, "max": 240},
            "dlss": {"type": "string", "options": ["Off", "Quality", "Balanced", "Performance", "Ultra Performance"]},
            "rtx": {"type": "bool"},
            "vrs": {"type": "bool"},
            "low_latency": {"type": "bool"},
            "dynamic_res": {"type": "bool"},
            "dynres_min": {"type": "int", "min": 30, "max": 120},
            "framecap": {"type": "bool"},
            "framecap_val": {"type": "int", "min": 30, "max": 240}
        }
        # Only a few for brevity; extend as needed
        profiles = [
            GameProfile("Elder Scrolls VI", ["elderscrolls6.exe"], [r"C:\Games\ES6\settings.ini"], schema["resolution"]["options"], True, schema),
            GameProfile("GTA VI", ["gtavi.exe"], [r"C:\Games\GTAVI\settings.xml"], schema["resolution"]["options"], True, schema),
            GameProfile("Cyberpunk 2077: Redux", ["cyberpunk2077.exe"], [r"C:\Games\CP2077\user.settings"], schema["resolution"]["options"], True, schema)
        ]
        return profiles

    def _detect_installed_games(self):
        found = []
        for profile in self.profiles:
            for path in profile.config_paths:
                if os.path.exists(path):
                    found.append(profile)
                    break
        return found if found else self.profiles

    def list_all_games(self):
        return [p.name for p in self.profiles]

    def get_profile_by_name(self, name):
        for p in self.profiles:
            if p.name.lower() == name.lower():
                return p
        return None

    def validate_settings(self, game_name, settings):
        profile = self.get_profile_by_name(game_name)
        if not profile:
            return False, "Unknown game"
        schema = profile.settings_schema
        for k, v in settings.items():
            if k not in schema:
                return False, f"Unknown setting: {k}"
            info = schema[k]
            if info["type"] == "int":
                if not isinstance(v, int):
                    return False, f"Setting {k} must be int"
                if "min" in info and v < info["min"]:
                    return False, f"Setting {k} too low"
                if "max" in info and v > info["max"]:
                    return False, f"Setting {k} too high"
            elif info["type"] == "string":
                if not isinstance(v, str):
                    return False, f"Setting {k} must be string"
                if "options" in info and v not in info["options"]:
                    return False, f"Setting {k} invalid value"
            elif info["type"] == "bool":
                if not isinstance(v, bool):
                    return False, f"Setting {k} must be bool"
        return True, ""