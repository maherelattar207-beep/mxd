import os
import sys
import json
import io
import time
import logging
import platform
import uuid
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class MXDLogger:
    """Enhanced logging system with in-memory logging and encrypted file output."""
    def __init__(self, name: str = "MXD_Pro", log_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        self.log_stream = io.StringIO()
        self.log_file = Path("logs") / "mxd_pro_encrypted.log"
        self.log_file.parent.mkdir(exist_ok=True)

        # We still want to see logs in the console during development/running
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # The stream handler will capture logs in memory
        stream_handler = logging.StreamHandler(self.log_stream)
        stream_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(stream_handler)

    def _get_encryption_key(self) -> str:
        # Use a machine-specific key for log encryption
        try:
            machine_id = str(uuid.getnode())
            return hashlib.sha256(machine_id.encode()).hexdigest()[:32]
        except Exception:
            return "default_log_key_fallback_32_chars" # Fallback key

    def _encrypt_logs(self, data: str) -> bytes:
        try:
            key = self._get_encryption_key()
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            derived_key = kdf.derive(key.encode())
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            pad_length = 16 - (len(data.encode()) % 16)
            padded_data = data.encode() + bytes([pad_length] * pad_length)
            return salt + iv + (encryptor.update(padded_data) + encryptor.finalize())
        except Exception as e:
            self.logger.error(f"Failed to encrypt logs: {e}")
            return b""

    def shutdown(self):
        """Encrypts the in-memory log stream and writes it to a file."""
        self.info("Application shutting down. Writing encrypted log.")
        log_contents = self.log_stream.getvalue()
        if not log_contents:
            return

        encrypted_logs = self._encrypt_logs(log_contents)
        if encrypted_logs:
            try:
                with open(self.log_file, "ab") as f: # Append to the log file
                    f.write(encrypted_logs + b'\n---LOG_ENTRY_SEPARATOR---\n')
            except Exception as e:
                self.logger.error(f"Could not write to encrypted log file: {e}")

    def info(self, message: str): self.logger.info(message)
    def warning(self, message: str): self.logger.warning(message)
    def error(self, message: str): self.logger.error(message)
    def log_system_info(self): self.info(f"MXD Pro starting on {platform.system()} {platform.release()}")

class SettingsManager:
    """Encrypted settings and configuration management."""
    def __init__(self, logger: MXDLogger):
        self.logger = logger
        self.settings_file = Path("settings.bin")
        self.encryption_key = self._get_machine_id()
        self.settings = self._load_settings()

    def _get_machine_id(self) -> str:
        try:
            system_info = [platform.system(), platform.machine(), platform.processor(), str(uuid.getnode())]
            if platform.system() == "Windows":
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                    machine_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
                    system_info.append(machine_guid)
                    winreg.CloseKey(key)
                except Exception: pass
            return hashlib.sha256("|".join(system_info).encode()).hexdigest()[:32]
        except Exception: return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]

    def _encrypt_data(self, data: str) -> bytes:
        try:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(self.encryption_key.encode())
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            pad_length = 16 - (len(data.encode()) % 16)
            padded_data = data.encode() + bytes([pad_length] * pad_length)
            return salt + iv + (encryptor.update(padded_data) + encryptor.finalize())
        except Exception as e:
            self.logger.error(f"Error encrypting settings: {e}")
            return b""

    def _decrypt_data(self, encrypted_data: bytes) -> str:
        try:
            salt, iv, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(self.encryption_key.encode())
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            pad_length = padded_data[-1]
            return padded_data[:-pad_length].decode()
        except Exception as e:
            self.logger.error(f"Error decrypting settings: {e}")
            return ""

    def _get_default_settings(self):
        return {"version": "2.0.0", "first_run": True, "language": "en", "performance_mode": "Normal", "ai_optimizer": {"learning_mode": True}, "security_suite": {"real_time_scan": False, "virus_total_check": True}}

    def _load_settings(self) -> Dict[str, Any]:
        defaults = self._get_default_settings()
        if not self.settings_file.exists():
            self.logger.info("No settings file found, creating defaults.")
            self._save_settings(defaults)
            return defaults
        try:
            with open(self.settings_file, 'rb') as f:
                decrypted_json = self._decrypt_data(f.read())
            if not decrypted_json: raise ValueError("Decryption failed.")
            loaded_settings = json.loads(decrypted_json)
            return {**defaults, **loaded_settings}
        except Exception as e:
            self.logger.error(f"Error loading settings, reverting to defaults: {e}")
            self._save_settings(defaults)
            return defaults

    def _save_settings(self, settings: Dict[str, Any]):
        try:
            settings_json = json.dumps(settings, indent=2)
            encrypted_data = self._encrypt_data(settings_json)
            with open(self.settings_file, 'wb') as f: f.write(encrypted_data)
        except Exception as e: self.logger.error(f"Error saving settings: {e}")

    def get(self, key: str, default=None):
        keys, value = key.split('.'), self.settings
        for k in keys:
            if isinstance(value, dict) and k in value: value = value[k]
            else: return default
        return value

    def set(self, key: str, value: Any):
        keys, d = key.split('.'), self.settings
        for k in keys[:-1]: d = d.setdefault(k, {})
        d[keys[-1]] = value
        self._save_settings(self.settings)

class SystemUtils:
    @staticmethod
    def clear_all_user_data(logger):
        logger.warning("Clearing all user data...")
        paths_to_delete = [
            Path("logs"), Path("settings.bin"), Path("license.txt"),
            Path(".license_data"), Path("ai_learning_data.json"),
            Path("game_profiles.json")
        ]
        for path in paths_to_delete:
            try:
                if path.is_dir(): shutil.rmtree(path)
                elif path.exists(): path.unlink()
                logger.info(f"Removed: {path}")
            except Exception as e: logger.error(f"Failed to remove {path}: {e}")

    @staticmethod
    def verify_digital_signature():
        """
        Placeholder for verifying the digital signature of the application files.
        In a real application, this would involve checking certificates against a trusted root.
        """
        # For this simulation, we'll assume the signature is always valid.
        return True

class SafeModeManager:
    def __init__(self, logger: MXDLogger, settings: SettingsManager): self.logger = logger
class GameProfilesDatabase:
    def __init__(self, logger: MXDLogger): self.logger = logger

def initialize_mxd_pro() -> tuple:
    logger = MXDLogger()
    logger.log_system_info()
    settings = SettingsManager(logger)
    safe_mode = SafeModeManager(logger, settings)
    profiles_db = GameProfilesDatabase(logger)
    return logger, settings, safe_mode, profiles_db
