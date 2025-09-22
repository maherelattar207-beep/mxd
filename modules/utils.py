#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro - Utils Module
Provides logging, settings management, and utility functions
"""

import os
import sys
import json
import time
import logging
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class MXDLogger:
    """Enhanced logging system with timestamps for all actions"""

    def __init__(self, name: str = "MXD_Pro", log_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create logs directory if it doesn't exist
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        # Create file handler
        log_file = self.log_dir / f"mxd_pro_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        """Log info message with timestamp"""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message with timestamp"""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message with timestamp"""
        self.logger.error(message)

    def debug(self, message: str):
        """Log debug message with timestamp"""
        self.logger.debug(message)

    def critical(self, message: str):
        """Log critical message with timestamp"""
        self.logger.critical(message)

    def log_system_info(self):
        """Log system information at startup"""
        self.info(f"MXD Pro starting on {platform.system()} {platform.release()}")
        self.info(f"Python version: {sys.version}")
        self.info(f"Platform: {platform.platform()}")

class SettingsManager:
    """Settings and configuration management with safe mode support"""

    def __init__(self, logger: MXDLogger):
        self.logger = logger
        self.settings_file = Path("settings.json")
        self.backup_dir = Path("settings_backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create defaults"""
        default_settings = {
            "version": "1.0.0",
            "first_run": True,
            "theme": "dark",
            "language": "en",
            "safe_mode": True,
            "auto_updates": True,
            "hardware_monitoring": True,
            "ai_optimizer": {
                "enabled": True,
                "learning_mode": True,
                "cpu_usage_limit": 10
            },
            "gaming_optimizer": {
                "enabled": True,
                "profiles": {},
                "auto_detect": True
            },
            "security_suite": {
                "enabled": True,
                "real_time_scan": False,
                "virus_total_check": True
            },
            "registry_cleaner": {
                "enabled": True,
                "backup_before_clean": True,
                "aggressive_mode": False
            },
            "ui_settings": {
                "window_width": 1200,
                "window_height": 800,
                "show_tooltips": True
            }
        }

        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_settings = {**default_settings, **loaded_settings}
                self.logger.info("Settings loaded successfully")
                return merged_settings
            except Exception as e:
                self.logger.error(f"Error loading settings: {e}")
                self.logger.info("Using default settings")
                return default_settings
        else:
            self.logger.info("No settings file found, creating defaults")
            self._save_settings(default_settings)
            return default_settings

    def _save_settings(self, settings: Dict[str, Any]):
        """Save settings to file with backup"""
        try:
            # Create backup first
            if self.settings_file.exists():
                backup_name = f"settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = self.backup_dir / backup_name
                with open(self.settings_file, 'r', encoding='utf-8') as src:
                    with open(backup_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())

            # Save new settings
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)

            self.logger.info("Settings saved successfully")

        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")

    def get(self, key: str, default=None):
        """Get setting value using dot notation (e.g., 'ai_optimizer.enabled')"""
        keys = key.split('.')
        value = self.settings

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set setting value using dot notation"""
        keys = key.split('.')
        current = self.settings

        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        # Set the final value
        current[keys[-1]] = value
        self._save_settings(self.settings)
        self.logger.info(f"Setting updated: {key} = {value}")

    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.settings.copy()

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.logger.warning("Resetting all settings to defaults")
        os.remove(self.settings_file)
        self.settings = self._load_settings()

class SafeModeManager:
    """Safe Mode manager for confirming critical operations"""

    def __init__(self, logger: MXDLogger, settings: SettingsManager):
        self.logger = logger
        self.settings = settings
        self.safe_mode_enabled = settings.get("safe_mode", True)

    def confirm_critical_action(self, action_name: str, description: str) -> bool:
        """
        Check if critical action should proceed
        Returns True if action should proceed, False otherwise
        """
        if not self.safe_mode_enabled:
            self.logger.info(f"Safe mode disabled, proceeding with: {action_name}")
            return True

        self.logger.warning(f"Safe mode confirmation required for: {action_name}")
        self.logger.info(f"Description: {description}")

        # In a GUI application, this would show a dialog
        # For now, we'll log the requirement
        self.logger.info("Safe mode confirmation would be required in GUI")
        return True  # Assume confirmation for automation

    def enable_safe_mode(self):
        """Enable safe mode"""
        self.safe_mode_enabled = True
        self.settings.set("safe_mode", True)
        self.logger.info("Safe mode enabled")

    def disable_safe_mode(self):
        """Disable safe mode"""
        self.safe_mode_enabled = False
        self.settings.set("safe_mode", False)
        self.logger.warning("Safe mode disabled")

class SystemUtils:
    """System utility functions"""

    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows"""
        return platform.system().lower() == "windows"

    @staticmethod
    def is_admin() -> bool:
        """Check if running with administrator privileges"""
        try:
            if SystemUtils.is_windows():
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False

    @staticmethod
    def get_app_data_dir() -> Path:
        """Get application data directory"""
        if SystemUtils.is_windows():
            app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
        else:
            app_data = os.path.expanduser("~/.local/share")

        mxd_dir = Path(app_data) / "MXDPro"
        mxd_dir.mkdir(exist_ok=True)
        return mxd_dir

    @staticmethod
    def create_directory_structure():
        """Create necessary directory structure"""
        directories = [
            "logs",
            "backups",
            "profiles",
            "cache",
            "temp"
        ]

        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)

    @staticmethod
    def cleanup_temp_files():
        """Clean up temporary files"""
        temp_dir = Path("temp")
        if temp_dir.exists():
            try:
                import shutil
                shutil.rmtree(temp_dir)
                temp_dir.mkdir(exist_ok=True)
            except Exception as e:
                print(f"Error cleaning temp files: {e}")

class GameProfilesDatabase:
    """Game profiles database with import/export functionality"""

    def __init__(self, logger: MXDLogger):
        self.logger = logger
        self.profiles_file = Path("profiles") / "game_profiles.json"
        self.profiles_file.parent.mkdir(exist_ok=True)
        self.profiles = self._load_profiles()

    def _load_profiles(self) -> Dict[str, Any]:
        """Load game profiles from file"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
                self.logger.info(f"Loaded {len(profiles)} game profiles")
                return profiles
            except Exception as e:
                self.logger.error(f"Error loading profiles: {e}")
                return {}
        else:
            self.logger.info("No game profiles file found, creating new database")
            return {}

    def save_profiles(self):
        """Save profiles to file"""
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)
            self.logger.info("Game profiles saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving profiles: {e}")

    def add_profile(self, game_name: str, profile_data: Dict[str, Any]):
        """Add or update a game profile"""
        self.profiles[game_name] = {
            **profile_data,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        self.save_profiles()
        self.logger.info(f"Added/updated profile for {game_name}")

    def get_profile(self, game_name: str) -> Optional[Dict[str, Any]]:
        """Get game profile by name"""
        return self.profiles.get(game_name)

    def remove_profile(self, game_name: str) -> bool:
        """Remove game profile"""
        if game_name in self.profiles:
            del self.profiles[game_name]
            self.save_profiles()
            self.logger.info(f"Removed profile for {game_name}")
            return True
        return False

    def list_profiles(self) -> list:
        """List all profile names"""
        return list(self.profiles.keys())

    def export_profiles(self, export_path: str) -> bool:
        """Export all profiles to a file"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Profiles exported to {export_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting profiles: {e}")
            return False

    def import_profiles(self, import_path: str) -> bool:
        """Import profiles from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_profiles = json.load(f)

            # Merge with existing profiles
            self.profiles.update(imported_profiles)
            self.save_profiles()
            self.logger.info(f"Imported {len(imported_profiles)} profiles from {import_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error importing profiles: {e}")
            return False

def initialize_mxd_pro() -> tuple:
    """
    Initialize MXD Pro core components
    Returns: (logger, settings, safe_mode_manager, profiles_db)
    """
    # Create directory structure
    SystemUtils.create_directory_structure()

    # Initialize logger
    logger = MXDLogger()
    logger.log_system_info()
    logger.info("MXD Pro initialization started")

    # Initialize settings
    settings = SettingsManager(logger)

    # Initialize safe mode manager
    safe_mode = SafeModeManager(logger, settings)

    # Initialize profiles database
    profiles_db = GameProfilesDatabase(logger)

    logger.info("MXD Pro core components initialized successfully")

    return logger, settings, safe_mode, profiles_db

if __name__ == "__main__":
    # Test the utils module
    logger, settings, safe_mode, profiles_db = initialize_mxd_pro()

    # Test settings
    logger.info("Testing settings manager...")
    settings.set("test.value", 42)
    test_value = settings.get("test.value")
    logger.info(f"Test value: {test_value}")

    # Test safe mode
    logger.info("Testing safe mode...")
    result = safe_mode.confirm_critical_action("Test Action", "This is a test action")
    logger.info(f"Safe mode result: {result}")

    # Test profiles
    logger.info("Testing profiles database...")
    profiles_db.add_profile("Test Game", {"resolution": "4K", "fps": 60})
    profile = profiles_db.get_profile("Test Game")
    logger.info(f"Test profile: {profile}")

    logger.info("Utils module testing completed")