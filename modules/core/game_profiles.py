import os
import json
from datetime import datetime
from ..optimizer import UpscalingTechnology, OptimizationLevel, GameProfile

class GameProfileManager:
    """Manages game detection, profile loading, and optimization settings."""
    def __init__(self, logger, hardware, profiles_path='data/game_profiles.json'):
        self.logger = logger
        self.hardware = hardware
        self.profiles_path = profiles_path
        os.makedirs(os.path.dirname(profiles_path), exist_ok=True)
        self.game_profiles = self._load_game_profiles()

    def _load_game_profiles(self):
        """Loads game profiles from a JSON file."""
        if not os.path.exists(self.profiles_path):
            self.logger.warning(f"Game profiles file not found at {self.profiles_path}. Creating a default one.")
            default_profiles = self._create_default_profiles()
            with open(self.profiles_path, 'w') as f:
                json.dump({"games": [p.to_dict() for p in default_profiles.values()]}, f, indent=4)
            return default_profiles

        try:
            with open(self.profiles_path, 'r') as f:
                data = json.load(f)
                profiles = {}
                for game_data in data.get("games", []):
                    profile = GameProfile.from_dict(game_data)
                    profiles[profile.name] = profile
                self.logger.info(f"Successfully loaded {len(profiles)} game profiles.")
                return profiles
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to load or parse game profiles: {e}. Starting with an empty list.")
            return {}

    def _create_default_profiles(self):
        """Creates a set of default game profiles if none exist."""
        # This would typically be more extensive
        return {
            "Cyberpunk 2077": GameProfile(
                name="Cyberpunk 2077",
                executable_paths=["Cyberpunk2077.exe"],
                upscaling=UpscalingTechnology.DLSS_QUALITY,
                frame_generation=True
            ),
            "The Witcher 3": GameProfile(
                name="The Witcher 3",
                executable_paths=["witcher3.exe"],
                upscaling=UpscalingTechnology.FSR2_QUALITY,
                frame_generation=False
            ),
        }

    def _save_game_profiles(self):
        """Saves the current game profiles to the JSON file."""
        try:
            with open(self.profiles_path, 'w') as f:
                json.dump({"games": [p.to_dict() for p in self.game_profiles.values()]}, f, indent=4)
            self.logger.info("Game profiles saved successfully.")
        except IOError as e:
            self.logger.error(f"Error saving game profiles: {e}")

    def detect_installed_games(self, search_paths=None):
        """Detects installed games based on executable paths in profiles."""
        # This is a placeholder for a more robust detection mechanism
        # e.g., scanning Steam libraries, Epic Games store, etc.
        self.logger.info("Game detection is a placeholder. All profiles are loaded by default.")
        return list(self.game_profiles.keys())

    def get_profile(self, game_name):
        """Retrieves a profile by game name."""
        return self.game_profiles.get(game_name)

    def import_game_profiles(self, file_path):
        """Imports game profiles from a user-selected JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                imported_count = 0
                for game_data in data.get("games", []):
                    profile = GameProfile.from_dict(game_data)
                    self.game_profiles[profile.name] = profile
                    imported_count += 1
                self._save_game_profiles()
                self.logger.info(f"Successfully imported {imported_count} game profiles from {file_path}.")
                return True
        except (json.JSONDecodeError, KeyError, IOError) as e:
            self.logger.error(f"Failed to import game profiles from {file_path}: {e}")
            return False

    def export_game_profiles(self, file_path):
        """Exports all current game profiles to a JSON file."""
        try:
            self._save_game_profiles() # Ensure we're exporting the latest
            with open(file_path, 'w') as f:
                 json.dump({"games": [p.to_dict() for p in self.game_profiles.values()]}, f, indent=4)
            self.logger.info(f"Successfully exported game profiles to {file_path}.")
            return True
        except IOError as e:
            self.logger.error(f"Failed to export game profiles to {file_path}: {e}")
            return False

    def apply_game_optimization(self, game_name, system_info):
        """Applies optimization settings for a specific game."""
        profile = self.get_profile(game_name)
        if not profile:
            self.logger.error(f"Cannot apply optimization: Profile for {game_name} not found.")
            return

        self.logger.info(f"Applying optimizations for {profile.name}...")
        self.logger.info(f"  - Upscaling: {profile.upscaling.name}")
        self.logger.info(f"  - Frame Generation: {'Enabled' if profile.frame_generation else 'Disabled'}")
        self.logger.info(f"  - Dynamic Resolution: {'Enabled' if profile.dynamic_resolution else 'Disabled'}")
        # In a real scenario, this would involve writing to game config files
        # or using APIs like NVIDIA's to apply these settings.
        self.logger.info(f"Configuration for '{game_name}' applied (simulation).")